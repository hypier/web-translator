---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/llms/writer.ipynb
---
# Writer

[Writer](https://writer.com/) is a platform to generate different language content.

This example goes over how to use LangChain to interact with `Writer` [models](https://dev.writer.com/docs/models).

You have to get the WRITER_API_KEY [here](https://dev.writer.com/docs).


```python
from getpass import getpass

WRITER_API_KEY = getpass()
```
```output
 ········
```

```python
import os

os.environ["WRITER_API_KEY"] = WRITER_API_KEY
```


```python
from langchain.chains import LLMChain
from langchain_community.llms import Writer
from langchain_core.prompts import PromptTemplate
```


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
```


```python
# If you get an error, probably, you need to set up the "base_url" parameter that can be taken from the error log.

llm = Writer()
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)
```


## Related

- LLM [conceptual guide](/docs/concepts/#llms)
- LLM [how-to guides](/docs/how_to/#llms)
