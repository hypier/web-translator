---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/how_to/few_shot_examples_chat.ipynb
sidebar_position: 2
---

# 如何在聊天模型中使用少量示例

:::info 前提条件

本指南假设您熟悉以下概念：
- [提示模板](/docs/concepts/#prompt-templates)
- [示例选择器](/docs/concepts/#example-selectors)
- [聊天模型](/docs/concepts/#chat-model)
- [向量存储](/docs/concepts/#vector-stores)

:::

本指南介绍如何通过示例输入和输出提示聊天模型。向模型提供少量此类示例称为少量示例提示（few-shotting），这是一种简单但强大的引导生成的方法，在某些情况下可以显著提高模型性能。

关于如何最佳地进行少量示例提示似乎没有明确的共识，最佳的提示编制可能因模型而异。因此，我们提供了像 [FewShotChatMessagePromptTemplate](https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.few_shot.FewShotChatMessagePromptTemplate.html?highlight=fewshot#langchain_core.prompts.few_shot.FewShotChatMessagePromptTemplate) 这样的少量示例提示模板作为灵活的起点，您可以根据需要进行修改或替换。

少量示例提示模板的目标是根据输入动态选择示例，然后将示例格式化为最终提示以提供给模型。

**注意：** 以下代码示例仅适用于聊天模型，因为 `FewShotChatMessagePromptTemplates` 旨在输出格式化的 [聊天消息](/docs/concepts/#message-types)，而不是纯字符串。有关与完成模型（LLMs）兼容的纯字符串模板的类似少量示例提示，请参阅 [少量示例提示模板](/docs/how_to/few_shot_examples/) 指南。

## 固定示例

最基本（也是最常见）的少量提示技术是使用固定的提示示例。这样，您可以选择一个链，评估它，并避免在生产中担心额外的可变部分。

模板的基本组成部分是：
- `examples`: 包含在最终提示中的字典示例列表。
- `example_prompt`: 通过其 [`format_messages`](https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html?highlight=format_messages#langchain_core.prompts.chat.ChatPromptTemplate.format_messages) 方法将每个示例转换为1个或多个消息。一个常见的示例是将每个示例转换为一个人类消息和一个AI消息响应，或者一个人类消息后跟一个函数调用消息。

下面是一个简单的演示。首先，定义您想要包含的示例。我们给LLM一个不熟悉的数学运算符，用“🦜”表情符号表示：


```python
%pip install -qU langchain langchain-openai langchain-chroma

import os
from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass()
```

如果我们尝试询问模型这个表达式的结果，它将失败：


```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.0)

model.invoke("What is 2 🦜 9?")
```



```output
AIMessage(content='The expression "2 🦜 9" is not a standard mathematical operation or equation. It appears to be a combination of the number 2 and the parrot emoji 🦜 followed by the number 9. It does not have a specific mathematical meaning.', response_metadata={'token_usage': {'completion_tokens': 54, 'prompt_tokens': 17, 'total_tokens': 71}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-aad12dda-5c47-4a1e-9949-6fe94e03242a-0', usage_metadata={'input_tokens': 17, 'output_tokens': 54, 'total_tokens': 71})
```


现在让我们看看如果给LLM一些示例会发生什么。我们将在下面定义一些：


```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]
```

接下来，将它们组装成少量提示模板。


```python
# 这是一个用于格式化每个单独示例的提示模板。
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

print(few_shot_prompt.invoke({}).to_messages())
```
```output
[HumanMessage(content='2 🦜 2'), AIMessage(content='4'), HumanMessage(content='2 🦜 3'), AIMessage(content='5')]
```
最后，我们将最终提示组装如下，将 `few_shot_prompt` 直接传递给 `from_messages` 工厂方法，并与模型一起使用：


```python
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)
```

现在让我们问模型最初的问题，看看它的表现如何：


```python
from langchain_openai import ChatOpenAI

chain = final_prompt | model

chain.invoke({"input": "What is 2 🦜 9?"})
```



```output
AIMessage(content='11', response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 60, 'total_tokens': 61}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-5ec4e051-262f-408e-ad00-3f2ebeb561c3-0', usage_metadata={'input_tokens': 60, 'output_tokens': 1, 'total_tokens': 61})
```


我们可以看到，模型现在从给定的少量示例中推断出鹦鹉表情符号表示加法！

## 动态少样本提示

有时您可能希望根据输入仅选择整体集合中的少数示例进行展示。为此，您可以将传递到 `FewShotChatMessagePromptTemplate` 中的 `examples` 替换为 `example_selector`。其他组件与上述保持一致！我们的动态少样本提示模板如下所示：

- `example_selector`：负责为给定输入选择少样本示例（以及返回顺序）。这些实现了 [BaseExampleSelector](https://api.python.langchain.com/en/latest/example_selectors/langchain_core.example_selectors.base.BaseExampleSelector.html?highlight=baseexampleselector#langchain_core.example_selectors.base.BaseExampleSelector) 接口。一个常见的例子是基于向量存储的 [SemanticSimilarityExampleSelector](https://api.python.langchain.com/en/latest/example_selectors/langchain_core.example_selectors.semantic_similarity.SemanticSimilarityExampleSelector.html?highlight=semanticsimilarityexampleselector#langchain_core.example_selectors.semantic_similarity.SemanticSimilarityExampleSelector)
- `example_prompt`：通过其 [`format_messages`](https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html?highlight=chatprompttemplate#langchain_core.prompts.chat.ChatPromptTemplate.format_messages) 方法将每个示例转换为 1 个或多个消息。一个常见的例子是将每个示例转换为一个人类消息和一个 AI 消息响应，或者一个人类消息后跟一个函数调用消息。

这些可以再次与其他消息和聊天模板组合，以组装您的最终提示。

让我们通过 `SemanticSimilarityExampleSelector` 举个例子。由于此实现使用向量存储根据语义相似性选择示例，我们首先需要填充存储。由于这里的基本思想是我们希望搜索并返回与文本输入最相似的示例，因此我们嵌入我们的提示示例的 `values`，而不是考虑键：

```python
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
    {"input": "2 🦜 4", "output": "6"},
    {"input": "What did the cow say to the moon?", "output": "nothing at all"},
    {
        "input": "Write me a poem about the moon",
        "output": "One for the moon, and one for me, who are we to talk about the moon?",
    },
]

to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)
```

### 创建 `example_selector`

在创建了 vectorstore 后，我们可以创建 `example_selector`。在这里我们将单独调用它，并将 `k` 设置为仅获取与输入最接近的两个示例。

```python
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

# 提示模板将通过传递输入到 `select_examples` 方法加载示例
example_selector.select_examples({"input": "horse"})
```

```output
[{'input': 'What did the cow say to the moon?', 'output': 'nothing at all'},
 {'input': '2 🦜 4', 'output': '6'}]
```

### 创建提示模板

我们现在组装提示模板，使用上面创建的 `example_selector`。

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 定义少量示例提示。
few_shot_prompt = FewShotChatMessagePromptTemplate(
    # 输入变量选择要传递给 example_selector 的值
    input_variables=["input"],
    example_selector=example_selector,
    # 定义每个示例的格式。
    # 在这种情况下，每个示例将变成 2 条消息：
    # 1 条人类消息和 1 条 AI 消息
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

print(few_shot_prompt.invoke(input="What's 3 🦜 3?").to_messages())
```
```output
[HumanMessage(content='2 🦜 3'), AIMessage(content='5'), HumanMessage(content='2 🦜 4'), AIMessage(content='6')]
```
我们可以将这个少量示例聊天消息提示模板传递给另一个聊天提示模板：

```python
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

print(few_shot_prompt.invoke(input="What's 3 🦜 3?"))
```
```output
messages=[HumanMessage(content='2 🦜 3'), AIMessage(content='5'), HumanMessage(content='2 🦜 4'), AIMessage(content='6')]
```

### 与聊天模型的使用

最后，您可以将模型连接到少量示例提示。

```python
chain = final_prompt | ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.0)

chain.invoke({"input": "What's 3 🦜 3?"})
```



```output
AIMessage(content='6', response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 60, 'total_tokens': 61}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-d1863e5e-17cd-4e9d-bf7a-b9f118747a65-0', usage_metadata={'input_tokens': 60, 'output_tokens': 1, 'total_tokens': 61})
```

## 下一步

您现在已经学习了如何向聊天提示添加少量示例。

接下来，请查看本节中关于提示模板的其他操作指南，以及与[文本补全模型的少量示例](/docs/how_to/few_shot_examples)相关的操作指南，或其他[示例选择器操作指南](/docs/how_to/example_selectors/)。