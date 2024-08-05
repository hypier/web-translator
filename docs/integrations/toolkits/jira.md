---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/toolkits/jira.ipynb
---

# Jira

本笔记本介绍了如何使用 `Jira` 工具包。

`Jira` 工具包允许代理与给定的 Jira 实例进行交互，执行诸如搜索问题和创建问题等操作，该工具封装了 atlassian-python-api 库，更多信息请参见：https://atlassian-python-api.readthedocs.io/jira.html

要使用此工具，您必须首先设置以下环境变量：
    JIRA_API_TOKEN
    JIRA_USERNAME
    JIRA_INSTANCE_URL
    JIRA_CLOUD


```python
%pip install --upgrade --quiet  atlassian-python-api
```


```python
%pip install -qU langchain-community
```


```python
import os

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_openai import OpenAI
```


```python
os.environ["JIRA_API_TOKEN"] = "abc"
os.environ["JIRA_USERNAME"] = "123"
os.environ["JIRA_INSTANCE_URL"] = "https://jira.atlassian.com"
os.environ["OPENAI_API_KEY"] = "xyz"
os.environ["JIRA_CLOUD"] = "True"
```


```python
llm = OpenAI(temperature=0)
jira = JiraAPIWrapper()
toolkit = JiraToolkit.from_jira_api_wrapper(jira)
agent = initialize_agent(
    toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run("make a new issue in project PW to remind me to make more fried rice")
```
```output


[1m> Entering new AgentExecutor chain...[0m
[32;1m[1;3m I need to create an issue in project PW
Action: Create Issue
Action Input: {"summary": "Make more fried rice", "description": "Reminder to make more fried rice", "issuetype": {"name": "Task"}, "priority": {"name": "Low"}, "project": {"key": "PW"}}[0m
Observation: [38;5;200m[1;3mNone[0m
Thought:[32;1m[1;3m I now know the final answer
Final Answer: A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".[0m

[1m> Finished chain.[0m
```


```output
'A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".'
```