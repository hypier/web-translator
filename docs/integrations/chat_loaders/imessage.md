---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat_loaders/imessage.ipynb
---
# iMessage

This notebook shows how to use the iMessage chat loader. This class helps convert iMessage conversations to LangChain chat messages.

On MacOS, iMessage stores conversations in a sqlite database at `~/Library/Messages/chat.db` (at least for macOS Ventura 13.4). 
The `IMessageChatLoader` loads from this database file. 

1. Create the `IMessageChatLoader` with the file path pointed to `chat.db` database you'd like to process.
2. Call `loader.load()` (or `loader.lazy_load()`) to perform the conversion. Optionally use `merge_chat_runs` to combine message from the same sender in sequence, and/or `map_ai_messages` to convert messages from the specified sender to the "AIMessage" class.

## 1. Access Chat DB

It's likely that your terminal is denied access to `~/Library/Messages`. To use this class, you can copy the DB to an accessible directory (e.g., Documents) and load from there. Alternatively (and not recommended), you can grant full disk access for your terminal emulator in System Settings > Security and Privacy > Full Disk Access.

We have created an example database you can use at [this linked drive file](https://drive.google.com/file/d/1NebNKqTA2NXApCmeH6mu0unJD2tANZzo/view?usp=sharing).


```python
# This uses some example data
import requests


def download_drive_file(url: str, output_path: str = "chat.db") -> None:
    file_id = url.split("/")[-2]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url)
    if response.status_code != 200:
        print("Failed to download the file.")
        return

    with open(output_path, "wb") as file:
        file.write(response.content)
        print(f"File {output_path} downloaded.")


url = (
    "https://drive.google.com/file/d/1NebNKqTA2NXApCmeH6mu0unJD2tANZzo/view?usp=sharing"
)

# Download file to chat.db
download_drive_file(url)
```
```output
File chat.db downloaded.
```
## 2. Create the Chat Loader

Provide the loader with the file path to the zip directory. You can optionally specify the user id that maps to an ai message as well an configure whether to merge message runs.


```python
from langchain_community.chat_loaders.imessage import IMessageChatLoader
```


```python
loader = IMessageChatLoader(
    path="./chat.db",
)
```

## 3. Load messages

The `load()` (or `lazy_load`) methods return a list of "ChatSessions" that currently just contain a list of messages per loaded conversation. All messages are mapped to "HumanMessage" objects to start. 

You can optionally choose to merge message "runs" (consecutive messages from the same sender) and select a sender to represent the "AI". The fine-tuned LLM will learn to generate these AI messages.


```python
from typing import List

from langchain_community.chat_loaders.utils import (
    map_ai_messages,
    merge_chat_runs,
)
from langchain_core.chat_sessions import ChatSession

raw_messages = loader.lazy_load()
# Merge consecutive messages from the same sender into a single message
merged_messages = merge_chat_runs(raw_messages)
# Convert messages from "Tortoise" to AI messages. Do you have a guess who these conversations are between?
chat_sessions: List[ChatSession] = list(
    map_ai_messages(merged_messages, sender="Tortoise")
)
```


```python
# Now all of the Tortoise's messages will take the AI message class
# which maps to the 'assistant' role in OpenAI's training format
chat_sessions[0]["messages"][:3]
```



```output
[AIMessage(content="Slow and steady, that's my motto.", additional_kwargs={'message_time': 1693182723, 'sender': 'Tortoise'}, example=False),
 HumanMessage(content='Speed is key!', additional_kwargs={'message_time': 1693182753, 'sender': 'Hare'}, example=False),
 AIMessage(content='A balanced approach is more reliable.', additional_kwargs={'message_time': 1693182783, 'sender': 'Tortoise'}, example=False)]
```


## 3. Prepare for fine-tuning

Now it's time to convert our chat  messages to OpenAI dictionaries. We can use the `convert_messages_for_finetuning` utility to do so.


```python
from langchain_community.adapters.openai import convert_messages_for_finetuning
```


```python
training_data = convert_messages_for_finetuning(chat_sessions)
print(f"Prepared {len(training_data)} dialogues for training")
```
```output
Prepared 10 dialogues for training
```
## 4. Fine-tune the model

It's time to fine-tune the model. Make sure you have `openai` installed
and have set your `OPENAI_API_KEY` appropriately


```python
%pip install --upgrade --quiet  langchain-openai
```


```python
import json
import time
from io import BytesIO

import openai

# We will write the jsonl file in memory
my_file = BytesIO()
for m in training_data:
    my_file.write((json.dumps({"messages": m}) + "\n").encode("utf-8"))

my_file.seek(0)
training_file = openai.files.create(file=my_file, purpose="fine-tune")

# OpenAI audits each training file for compliance reasons.
# This make take a few minutes
status = openai.files.retrieve(training_file.id).status
start_time = time.time()
while status != "processed":
    print(f"Status=[{status}]... {time.time() - start_time:.2f}s", end="\r", flush=True)
    time.sleep(5)
    status = openai.files.retrieve(training_file.id).status
print(f"File {training_file.id} ready after {time.time() - start_time:.2f} seconds.")
```
```output
File file-zHIgf4r8LltZG3RFpkGd4Sjf ready after 10.19 seconds.
```
With the file ready, it's time to kick off a training job.


```python
job = openai.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-3.5-turbo",
)
```

Grab a cup of tea while your model is being prepared. This may take some time!


```python
status = openai.fine_tuning.jobs.retrieve(job.id).status
start_time = time.time()
while status != "succeeded":
    print(f"Status=[{status}]... {time.time() - start_time:.2f}s", end="\r", flush=True)
    time.sleep(5)
    job = openai.fine_tuning.jobs.retrieve(job.id)
    status = job.status
```
```output
Status=[running]... 524.95s
```

```python
print(job.fine_tuned_model)
```
```output
ft:gpt-3.5-turbo-0613:personal::7sKoRdlz
```
## 5. Use in LangChain

You can use the resulting model ID directly the `ChatOpenAI` model class.


```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=job.fine_tuned_model,
    temperature=1,
)
```


```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are speaking to hare."),
        ("human", "{input}"),
    ]
)

chain = prompt | model | StrOutputParser()
```


```python
for tok in chain.stream({"input": "What's the golden thread?"}):
    print(tok, end="", flush=True)
```
```output
A symbol of interconnectedness.
```