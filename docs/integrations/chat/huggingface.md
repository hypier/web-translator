---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/huggingface.ipynb
---

# ChatHuggingFace

这将帮助您开始使用 `langchain_huggingface` [聊天模型](/docs/concepts/#chat-models)。有关所有 `ChatHuggingFace` 功能和配置的详细文档，请访问 [API 参考](https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html)。要查看 Hugging Face 支持的模型列表，请查看 [此页面](https://huggingface.co/models)。

## 概述

### 集成细节

### 集成详情

| 类 | 包 | 本地 | 可序列化 | JS 支持 | 包下载量 | 包最新版本 |
| :--- | :--- | :---: | :---: |  :---: | :---: | :---: |
| [ChatHuggingFace](https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html) | [langchain-huggingface](https://api.python.langchain.com/en/latest/huggingface_api_reference.html) | ✅ | beta | ❌ | ![PyPI - Downloads](https://img.shields.io/pypi/dm/langchain_huggingface?style=flat-square&label=%20) | ![PyPI - Version](https://img.shields.io/pypi/v/langchain_huggingface?style=flat-square&label=%20) |

### 模型特性
| [工具调用](/docs/how_to/tool_calling) | [结构化输出](/docs/how_to/structured_output/) | JSON 模式 | [图像输入](/docs/how_to/multimodal_inputs/) | 音频输入 | 视频输入 | [令牌级流式传输](/docs/how_to/chat_streaming/) | 原生异步 | [令牌使用](/docs/how_to/chat_token_usage_tracking/) | [Logprobs](/docs/how_to/logprobs/) |
| :---: | :---: | :---: | :---: |  :---: | :---: | :---: | :---: | :---: | :---: |
| ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |

## 设置

要访问 Hugging Face 模型，您需要创建一个 Hugging Face 账户，获取一个 API 密钥，并安装 `langchain-huggingface` 集成包。

### 凭证

生成一个 [Hugging Face 访问令牌](https://huggingface.co/docs/hub/security-tokens) 并将其存储为环境变量： `HUGGINGFACEHUB_API_TOKEN`。


```python
import getpass
import os

if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")
```

### 安装

| 类别 | 包 | 本地 | 可序列化 | JS 支持 | 包下载量 | 包最新版本 |
| :--- | :--- | :---: | :---: |  :---: | :---: | :---: |
| [ChatHuggingFace](https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html) | [langchain_huggingface](https://api.python.langchain.com/en/latest/huggingface_api_reference.html) | ✅ | ❌ | ❌ | ![PyPI - Downloads](https://img.shields.io/pypi/dm/langchain_huggingface?style=flat-square&label=%20) | ![PyPI - Version](https://img.shields.io/pypi/v/langchain_huggingface?style=flat-square&label=%20) |

### 模型特性
| [工具调用](/docs/how_to/tool_calling) | [结构化输出](/docs/how_to/structured_output/) | JSON模式 | [图像输入](/docs/how_to/multimodal_inputs/) | 音频输入 | 视频输入 | [令牌级流式传输](/docs/how_to/chat_streaming/) | 原生异步 | [令牌使用](/docs/how_to/chat_token_usage_tracking/) | [对数概率](/docs/how_to/logprobs/) |
| :---: | :---: | :---: | :---: |  :---: | :---: | :---: | :---: | :---: | :---: |
| ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 设置

要访问 `langchain_huggingface` 模型，您需要创建一个 `Hugging Face` 账户，获取一个 API 密钥，并安装 `langchain_huggingface` 集成包。

### 证书

您需要将 [Hugging Face 访问令牌](https://huggingface.co/docs/hub/security-tokens) 保存为环境变量： `HUGGINGFACEHUB_API_TOKEN`。


```python
import getpass
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass(
    "Enter your Hugging Face API key: "
)
```


```python
%pip install --upgrade --quiet  langchain-huggingface text-generation transformers google-search-results numexpr langchainhub sentencepiece jinja2 bitsandbytes accelerate
```
```output

[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m24.0[0m[39;49m -> [0m[32;49m24.1.2[0m
[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
Note: you may need to restart the kernel to use updated packages.
```

## 实例化

您可以通过 `HuggingFaceEndpoint` 或 `HuggingFacePipeline` 以两种不同方式实例化 `ChatHuggingFace` 模型。

### `HuggingFaceEndpoint`


```python
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

chat_model = ChatHuggingFace(llm=llm)
```
```output
该令牌尚未保存到 git 凭据助手中。如果您希望同时设置 git 凭据，请直接在此函数中传递 `add_to_git_credential=True`，或者在通过 `huggingface-cli` 使用时使用 `--add-to-git-credential`。
令牌有效（权限：fineGrained）。
您的令牌已保存至 /Users/isaachershenson/.cache/huggingface/token
登录成功
```

### `HuggingFacePipeline`

```python
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    ),
)

chat_model = ChatHuggingFace(llm=llm)
```

```output
config.json:   0%|          | 0.00/638 [00:00<?, ?B/s]
```

```output
model.safetensors.index.json:   0%|          | 0.00/23.9k [00:00<?, ?B/s]
```

```output
Downloading shards:   0%|          | 0/8 [00:00<?, ?it/s]
```

```output
model-00001-of-00008.safetensors:   0%|          | 0.00/1.89G [00:00<?, ?B/s]
```

```output
model-00002-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

```output
model-00003-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

```output
model-00004-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

```output
model-00005-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

```output
model-00006-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

```output
model-00007-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

```output
model-00008-of-00008.safetensors:   0%|          | 0.00/816M [00:00<?, ?B/s]
```

```output
Loading checkpoint shards:   0%|          | 0/8 [00:00<?, ?it/s]
```

```output
generation_config.json:   0%|          | 0.00/111 [00:00<?, ?B/s]
```

### 使用量化进行实例化

要运行模型的量化版本，您可以按如下方式指定 `bitsandbytes` 量化配置：

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)
```

并将其作为 `model_kwargs` 的一部分传递给 `HuggingFacePipeline`：

```python
llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    ),
    model_kwargs={"quantization_config": quantization_config},
)

chat_model = ChatHuggingFace(llm=llm)
```

## 调用


```python
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(
        content="What happens when an unstoppable force meets an immovable object?"
    ),
]

ai_msg = chat_model.invoke(messages)
```


```python
print(ai_msg.content)
```
```output
According to the popular phrase and hypothetical scenario, when an unstoppable force meets an immovable object, a paradoxical situation arises as both forces are seemingly contradictory. On one hand, an unstoppable force is an entity that cannot be stopped or prevented from moving forward, while on the other hand, an immovable object is something that cannot be moved or displaced from its position. 

In this scenario, it is un
```

## API 参考

有关所有 `ChatHuggingFace` 功能和配置的详细文档，请访问 API 参考： https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html

## API 参考

有关所有 ChatHuggingFace 功能和配置的详细文档，请访问 API 参考： https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html

## 相关

- 聊天模型 [概念指南](/docs/concepts/#chat-models)
- 聊天模型 [操作指南](/docs/how_to/#chat-models)