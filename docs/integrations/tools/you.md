---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/you.ipynb
---
# You.com Search

The [you.com API](https://api.you.com) is a suite of tools designed to help developers ground the output of LLMs in the most recent, most accurate, most relevant information that may not have been included in their training dataset.

## Setup

The tool lives in the `langchain-community` package.

You also need to set your you.com API key.


```python
%pip install --upgrade --quiet langchain-community
```


```python
import os

os.environ["YDC_API_KEY"] = ""

# For use in Chaining section
os.environ["OPENAI_API_KEY"] = ""

## ALTERNATIVE: load YDC_API_KEY from a .env file

# !pip install --quiet -U python-dotenv
# import dotenv
# dotenv.load_dotenv()
```

It's also helpful (but not needed) to set up [LangSmith](https://smith.langchain.com/) for best-in-class observability


```python
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
```

## Tool Usage


```python
from langchain_community.tools.you import YouSearchTool
from langchain_community.utilities.you import YouSearchAPIWrapper

api_wrapper = YouSearchAPIWrapper(num_web_results=1)
tool = YouSearchTool(api_wrapper=api_wrapper)

tool
```



```output
YouSearchTool(api_wrapper=YouSearchAPIWrapper(ydc_api_key='054da371-e73b-47c1-a6d9-3b0cddf0fa3e<__>1Obt7EETU8N2v5f4MxaH0Zhx', num_web_results=1, safesearch=None, country=None, k=None, n_snippets_per_hit=None, endpoint_type='search', n_hits=None))
```



```python
# .invoke wraps utility.results
response = tool.invoke("What is the weather in NY")

# .invoke should have a Document for each `snippet`
print(len(response))

for item in response:
    print(item)
```

## Chaining

We show here how to use it as part of an [agent](/docs/tutorials/agents). We use the OpenAI Functions Agent, so we will need to setup and install the required dependencies for that. We will also use [LangSmith Hub](https://smith.langchain.com/hub) to pull the prompt from, so we will need to install that.


```python
# you need a model to use in the chain
!pip install --upgrade --quiet langchain langchain-openai langchainhub langchain-community
```


```python
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(temperature=0)
you_tool = YouSearchTool(api_wrapper=YouSearchAPIWrapper(num_web_results=1))
tools = [you_tool]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
```


```python
agent_executor.invoke({"input": "What is the weather in NY today?"})
```



## Related

- Tool [conceptual guide](/docs/concepts/#tools)
- Tool [how-to guides](/docs/how_to/#tools)
