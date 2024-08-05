---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/toolkits/robocorp.ipynb
---

# Robocorp

本笔记本介绍如何使用 [Robocorp Action Server](https://github.com/robocorp/robocorp) 行动工具包和 LangChain 入门。

Robocorp 是扩展 AI 代理、助手和副驾驶功能的最简单方法，支持自定义操作。

## 安装

首先，请参阅 [Robocorp 快速入门](https://github.com/robocorp/robocorp#quickstart)，了解如何设置 `Action Server` 并创建您的 Actions。

在您的 LangChain 应用中，安装 `langchain-robocorp` 包： 

```python
# Install package
%pip install --upgrade --quiet langchain-robocorp
```

当您按照上述快速入门创建新的 `Action Server` 时，它将创建一个包含文件的目录，包括 `action.py`。

我们可以添加 Python 函数作为 actions，如 [这里](https://github.com/robocorp/robocorp/tree/master/actions#describe-your-action) 所示。

让我们在 `action.py` 中添加一个示例函数。

```python
@action
def get_weather_forecast(city: str, days: int, scale: str = "celsius") -> str:
    """
    Returns weather conditions forecast for a given city.

    Args:
        city (str): Target city to get the weather conditions for
        days: How many day forecast to return
        scale (str): Temperature scale to use, should be one of "celsius" or "fahrenheit"

    Returns:
        str: The requested weather conditions forecast
    """
    return "75F and sunny :)"
```

然后我们启动服务器：

```bash
action-server start
```

我们可以看到： 

```
Found new action: get_weather_forecast

```

通过访问运行在 `http://localhost:8080` 的服务器并使用 UI 来运行该函数进行本地测试。

## 环境设置

可选地，您可以设置以下环境变量：

- `LANGCHAIN_TRACING_V2=true`：启用 LangSmith 日志运行追踪，也可以与相应的 Action Server 操作运行日志绑定。有关更多信息，请参见 [LangSmith 文档](https://docs.smith.langchain.com/tracing#log-runs)。

## 用法

我们启动了本地操作服务器，运行在 `http://localhost:8080` 上。


```python
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_robocorp import ActionServerToolkit

# Initialize LLM chat model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Initialize Action Server Toolkit
toolkit = ActionServerToolkit(url="http://localhost:8080", report_trace=True)
tools = toolkit.get_tools()

# Initialize Agent
system_message = SystemMessage(content="You are a helpful assistant")
prompt = OpenAIFunctionsAgent.create_prompt(system_message)
agent = OpenAIFunctionsAgent(llm=llm, prompt=prompt, tools=tools)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke("What is the current weather today in San Francisco in fahrenheit?")
```
```output


[1m> Entering new AgentExecutor chain...[0m
[32;1m[1;3m
Invoking: `robocorp_action_server_get_weather_forecast` with `{'city': 'San Francisco', 'days': 1, 'scale': 'fahrenheit'}`


[0m[33;1m[1;3m"75F and sunny :)"[0m[32;1m[1;3mThe current weather today in San Francisco is 75F and sunny.[0m

[1m> Finished chain.[0m
```


```output
{'input': 'What is the current weather today in San Francisco in fahrenheit?',
 'output': 'The current weather today in San Francisco is 75F and sunny.'}
```

### 单输入工具

默认情况下，`toolkit.get_tools()` 将返回作为结构化工具的操作。

要返回单输入工具，请传递一个用于处理输入的聊天模型。


```python
# Initialize single input Action Server Toolkit
toolkit = ActionServerToolkit(url="http://localhost:8080")
tools = toolkit.get_tools(llm=llm)
```