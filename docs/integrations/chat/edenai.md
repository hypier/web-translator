---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/edenai.ipynb
---

# Eden AI

Eden AI 正在通过联合最优秀的 AI 提供商来彻底改变 AI 领域，使用户能够解锁无限可能性，挖掘人工智能的真正潜力。凭借一个全面且无忧的平台，它允许用户快速将 AI 功能部署到生产环境中，通过单一 API 轻松访问全方位的 AI 能力。(网站: https://edenai.co/)

本示例介绍如何使用 LangChain 与 Eden AI 模型进行交互

-----------------------------------------------------------------------------------

`EdenAI` 超越了简单的模型调用。它为您提供了高级功能，包括：

- **多个提供商**：访问各种提供商提供的多样语言模型，让您可以自由选择最适合您用例的模型。

- **回退机制**：设置回退机制，确保即使主要提供商不可用，您也可以轻松切换到备选提供商，从而确保操作的无缝进行。

- **使用统计**：按项目和 API 密钥跟踪使用统计数据。此功能使您能够有效监控和管理资源消耗。

- **监控和可观察性**：`EdenAI` 在平台上提供全面的监控和可观察性工具。监控您的语言模型性能，分析使用模式，并获得有价值的见解以优化您的应用程序。


访问 EDENAI 的 API 需要一个 API 密钥，

您可以通过创建账户 https://app.edenai.run/user/register 获取密钥，并前往 https://app.edenai.run/admin/iam/api-keys

一旦我们有了密钥，我们将通过运行以下命令将其设置为环境变量：

```bash
export EDENAI_API_KEY="..."
```

您可以在 API 参考中找到更多详细信息 : https://docs.edenai.co/reference

如果您不想设置环境变量，可以在初始化 EdenAI Chat Model 类时通过名为 edenai_api_key 的参数直接传递密钥。


```python
from langchain_community.chat_models.edenai import ChatEdenAI
from langchain_core.messages import HumanMessage
```


```python
chat = ChatEdenAI(
    edenai_api_key="...", provider="openai", temperature=0.2, max_tokens=250
)
```


```python
messages = [HumanMessage(content="Hello !")]
chat.invoke(messages)
```



```output
AIMessage(content='Hello! How can I assist you today?')
```



```python
await chat.ainvoke(messages)
```



```output
AIMessage(content='Hello! How can I assist you today?')
```

## 流式处理与批处理

`ChatEdenAI` 支持流式处理和批处理。以下是一个示例。

```python
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
```
```output
Hello! How can I assist you today?
```

```python
chat.batch([messages])
```

```output
[AIMessage(content='Hello! How can I assist you today?')]
```

## 备用机制

使用 Eden AI，您可以设置备用机制，以确保即使主要提供商不可用，操作也能无缝进行，您可以轻松切换到替代提供商。

```python
chat = ChatEdenAI(
    edenai_api_key="...",
    provider="openai",
    temperature=0.2,
    max_tokens=250,
    fallback_providers="google",
)
```

在这个例子中，如果 OpenAI 遇到任何问题，您可以使用 Google 作为备份提供商。

有关 Eden AI 的更多信息和详细信息，请查看此链接： : https://docs.edenai.co/docs/additional-parameters

## 链式调用



```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "What is a good name for a company that makes {product}?"
)
chain = prompt | chat
```


```python
chain.invoke({"product": "healthy snacks"})
```



```output
AIMessage(content='VitalBites')
```

## 工具

### bind_tools()

通过 `ChatEdenAI.bind_tools`，我们可以轻松地将 Pydantic 类、字典模式、LangChain 工具，甚至函数作为工具传递给模型。

```python
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatEdenAI(provider="openai", temperature=0.2, max_tokens=500)


class GetWeather(BaseModel):
    """获取给定位置的当前天气"""

    location: str = Field(..., description="城市和州，例如：旧金山，加州")


llm_with_tools = llm.bind_tools([GetWeather])
```


```python
ai_msg = llm_with_tools.invoke(
    "旧金山的天气怎么样",
)
ai_msg
```



```output
AIMessage(content='', response_metadata={'openai': {'status': 'success', 'generated_text': None, 'message': [{'role': 'user', 'message': 'what is the weather like in San Francisco', 'tools': [{'name': 'GetWeather', 'description': 'Get the current weather in a given location', 'parameters': {'type': 'object', 'properties': {'location': {'description': 'The city and state, e.g. San Francisco, CA', 'type': 'string'}}, 'required': ['location']}}], 'tool_calls': None}, {'role': 'assistant', 'message': None, 'tools': None, 'tool_calls': [{'id': 'call_tRpAO7KbQwgTjlka70mCQJdo', 'name': 'GetWeather', 'arguments': '{"location":"San Francisco"}'}]}], 'cost': 0.000194}}, id='run-5c44c01a-d7bb-4df6-835e-bda596080399-0', tool_calls=[{'name': 'GetWeather', 'args': {'location': 'San Francisco'}, 'id': 'call_tRpAO7KbQwgTjlka70mCQJdo'}])
```



```python
ai_msg.tool_calls
```



```output
[{'name': 'GetWeather',
  'args': {'location': 'San Francisco'},
  'id': 'call_tRpAO7KbQwgTjlka70mCQJdo'}]
```

### with_structured_output()

BaseChatModel.with_structured_output 接口使从聊天模型获取结构化输出变得简单。您可以使用 ChatEdenAI.with_structured_output（在底层使用工具调用）来使模型更可靠地以特定格式返回输出：

```python
structured_llm = llm.with_structured_output(GetWeather)
structured_llm.invoke(
    "what is the weather like in San Francisco",
)
```

```output
GetWeather(location='San Francisco')
```

### 将工具结果传递给模型

这是一个如何使用工具的完整示例。将工具的输出传递给模型，并从模型中获取结果。

```python
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


llm = ChatEdenAI(
    provider="openai",
    max_tokens=1000,
    temperature=0.2,
)

llm_with_tools = llm.bind_tools([add], tool_choice="required")

query = "What is 11 + 11?"

messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

tool_call = ai_msg.tool_calls[0]
tool_output = add.invoke(tool_call["args"])

# This append the result from our tool to the model
messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

llm_with_tools.invoke(messages).content
```

```output
'11 + 11 = 22'
```

### 流式传输

Eden AI 目前不支持流式工具调用。尝试进行流式传输将只返回一条最终消息。

```python
list(llm_with_tools.stream("What's 9 + 9"))
```
```output
/home/eden/Projects/edenai-langchain/libs/community/langchain_community/chat_models/edenai.py:603: UserWarning: stream: Tool use is not yet supported in streaming mode.
  warnings.warn("stream: Tool use is not yet supported in streaming mode.")
```


```output
[AIMessageChunk(content='', id='run-fae32908-ec48-4ab2-ad96-bb0d0511754f', tool_calls=[{'name': 'add', 'args': {'a': 9, 'b': 9}, 'id': 'call_n0Tm7I9zERWa6UpxCAVCweLN'}], tool_call_chunks=[{'name': 'add', 'args': '{"a": 9, "b": 9}', 'id': 'call_n0Tm7I9zERWa6UpxCAVCweLN', 'index': 0}])]
```

## 相关

- 聊天模型 [概念指南](/docs/concepts/#chat-models)
- 聊天模型 [操作指南](/docs/how_to/#chat-models)