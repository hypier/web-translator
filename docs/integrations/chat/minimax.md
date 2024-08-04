---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/minimax.ipynb
sidebar_label: MiniMax
---
# MiniMaxChat

[Minimax](https://api.minimax.chat) is a Chinese startup that provides LLM service for companies and individuals.

This example goes over how to use LangChain to interact with MiniMax Inference for Chat.


```python
import os

os.environ["MINIMAX_GROUP_ID"] = "MINIMAX_GROUP_ID"
os.environ["MINIMAX_API_KEY"] = "MINIMAX_API_KEY"
```


```python
from langchain_community.chat_models import MiniMaxChat
from langchain_core.messages import HumanMessage
```


```python
chat = MiniMaxChat()
```


```python
chat(
    [
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        )
    ]
)
```


## Related

- Chat model [conceptual guide](/docs/concepts/#chat-models)
- Chat model [how-to guides](/docs/how_to/#chat-models)