---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/semanticscholar.ipynb
---
# Semantic Scholar API Tool

This notebook demos how to use the semantic scholar tool with an agent.


```python
# start by installing semanticscholar api
%pip install --upgrade --quiet  semanticscholar
```


```python
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
```


```python
instructions = """You are an expert researcher."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
```


```python
llm = ChatOpenAI(temperature=0)
```


```python
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun

tools = [SemanticScholarQueryRun()]
```


```python
agent = create_openai_functions_agent(llm, tools, prompt)
```


```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
```


```python
agent_executor.invoke(
    {
        "input": "What are some biases in the large language models? How have people tried to mitigate them? "
        "show me a list of papers and techniques. Based on your findings write new research questions "
        "to work on. Break down the task into subtasks for search. Use the search tool"
    }
)
```





## Related

- Tool [conceptual guide](/docs/concepts/#tools)
- Tool [how-to guides](/docs/how_to/#tools)
