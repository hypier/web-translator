---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/bash.ipynb
---

# Shell (bash)

给予代理访问 shell 的权限是强大的（尽管在沙盒环境外存在风险）。

LLM 可以用它来执行任何 shell 命令。一个常见的用例是让 LLM 与您的本地文件系统进行交互。

**注意：** Shell 工具不适用于 Windows 操作系统。


```python
%pip install --upgrade --quiet langchain-community
```


```python
from langchain_community.tools import ShellTool

shell_tool = ShellTool()
```


```python
print(shell_tool.run({"commands": ["echo 'Hello World!'", "time"]}))
```
```output
Hello World!

real	0m0.000s
user	0m0.000s
sys	0m0.000s
``````output
/Users/wfh/code/lc/lckg/langchain/tools/shell/tool.py:34: UserWarning: The shell tool has no safeguards by default. Use at your own risk.
  warnings.warn(
```

### 与代理一起使用

与所有工具一样，这些工具可以交给代理以完成更复杂的任务。让我们让代理从网页中获取一些链接。


```python
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")
self_ask_with_search = initialize_agent(
    [shell_tool], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
self_ask_with_search.run(
    "Download the langchain.com webpage and grep for all urls. Return only a sorted list of them. Be sure to use double quotes."
)
```
```output


[1m> Entering new AgentExecutor chain...[0m
[32;1m[1;3mQuestion: What is the task?
Thought: We need to download the langchain.com webpage and extract all the URLs from it. Then we need to sort the URLs and return them.
Action:
```
{
  "action": "shell",
  "action_input": {
    "commands": [
      "curl -s https://langchain.com | grep -o 'http[s]*://[^\" ]*' | sort"
    ]
  }
}
```
[0m
``````output
/Users/wfh/code/lc/lckg/langchain/tools/shell/tool.py:34: UserWarning: The shell tool has no safeguards by default. Use at your own risk.
  warnings.warn(
``````output

Observation: [36;1m[1;3mhttps://blog.langchain.dev/
https://discord.gg/6adMQxSpJS
https://docs.langchain.com/docs/
https://github.com/hwchase17/chat-langchain
https://github.com/hwchase17/langchain
https://github.com/hwchase17/langchainjs
https://github.com/sullivan-sean/chat-langchainjs
https://js.langchain.com/docs/
https://python.langchain.com/en/latest/
https://twitter.com/langchainai
[0m
Thought:[32;1m[1;3mThe URLs have been successfully extracted and sorted. We can return the list of URLs as the final answer.
Final Answer: ["https://blog.langchain.dev/", "https://discord.gg/6adMQxSpJS", "https://docs.langchain.com/docs/", "https://github.com/hwchase17/chat-langchain", "https://github.com/hwchase17/langchain", "https://github.com/hwchase17/langchainjs", "https://github.com/sullivan-sean/chat-langchainjs", "https://js.langchain.com/docs/", "https://python.langchain.com/en/latest/", "https://twitter.com/langchainai"][0m

[1m> Finished chain.[0m
```


```output
'["https://blog.langchain.dev/", "https://discord.gg/6adMQxSpJS", "https://docs.langchain.com/docs/", "https://github.com/hwchase17/chat-langchain", "https://github.com/hwchase17/langchain", "https://github.com/hwchase17/langchainjs", "https://github.com/sullivan-sean/chat-langchainjs", "https://js.langchain.com/docs/", "https://python.langchain.com/en/latest/", "https://twitter.com/langchainai"]'
```

## 相关

- 工具 [概念指南](/docs/concepts/#tools)
- 工具 [操作指南](/docs/how_to/#tools)