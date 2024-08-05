---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/callbacks/sagemaker_tracking.ipynb
---

# SageMaker Tracking

>[Amazon SageMaker](https://aws.amazon.com/sagemaker/) 是一个完全托管的服务，用于快速轻松地构建、训练和部署机器学习（ML）模型。

>[Amazon SageMaker Experiments](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html) 是 `Amazon SageMaker` 的一项功能，允许您组织、跟踪、比较和评估 ML 实验和模型版本。

本笔记本展示了如何使用 LangChain Callback 将提示和其他 LLM 超参数记录并跟踪到 `SageMaker Experiments` 中。在这里，我们使用不同的场景来展示这一功能：

* **Scenario 1**: *Single LLM* - 一个使用单个 LLM 模型根据给定提示生成输出的案例。
* **Scenario 2**: *Sequential Chain* - 一个使用两个 LLM 模型的顺序链的案例。
* **Scenario 3**: *Agent with Tools (Chain of Thought)* - 一个在 LLM 之外使用多个工具（搜索和数学）的案例。

在本笔记本中，我们将创建一个单一实验来记录每个场景的提示。

## 安装与设置


```python
%pip install --upgrade --quiet  sagemaker
%pip install --upgrade --quiet  langchain-openai
%pip install --upgrade --quiet  google-search-results
```

首先，设置所需的 API 密钥

* OpenAI: https://platform.openai.com/account/api-keys (用于 OpenAI LLM 模型)
* Google SERP API: https://serpapi.com/manage-api-key (用于 Google 搜索工具)


```python
import os

## 在下面添加您的 API 密钥
os.environ["OPENAI_API_KEY"] = "<ADD-KEY-HERE>"
os.environ["SERPAPI_API_KEY"] = "<ADD-KEY-HERE>"
```


```python
from langchain_community.callbacks.sagemaker_callback import SageMakerCallbackHandler
```


```python
from langchain.agents import initialize_agent, load_tools
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from sagemaker.analytics import ExperimentAnalytics
from sagemaker.experiments.run import Run
from sagemaker.session import Session
```

## LLM 提示跟踪


```python
# LLM 超参数
HPARAMS = {
    "temperature": 0.1,
    "model_name": "gpt-3.5-turbo-instruct",
}

# 用于保存提示日志的桶（使用 `None` 保存默认桶，或更改为其他桶）
BUCKET_NAME = None

# 实验名称
EXPERIMENT_NAME = "langchain-sagemaker-tracker"

# 使用给定桶创建 SageMaker 会话
session = Session(default_bucket=BUCKET_NAME)
```

### 场景 1 - LLM


```python
RUN_NAME = "run-scenario-1"
PROMPT_TEMPLATE = "tell me a joke about {topic}"
INPUT_VARIABLES = {"topic": "fish"}
```


```python
with Run(
    experiment_name=EXPERIMENT_NAME, run_name=RUN_NAME, sagemaker_session=session
) as run:
    # 创建 SageMaker 回调
    sagemaker_callback = SageMakerCallbackHandler(run)

    # 定义带回调的 LLM 模型
    llm = OpenAI(callbacks=[sagemaker_callback], **HPARAMS)

    # 创建提示模板
    prompt = PromptTemplate.from_template(template=PROMPT_TEMPLATE)

    # 创建 LLM 链
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[sagemaker_callback])

    # 运行链
    chain.run(**INPUT_VARIABLES)

    # 重置回调
    sagemaker_callback.flush_tracker()
```

### 场景 2 - 顺序链

```python
RUN_NAME = "run-scenario-2"

PROMPT_TEMPLATE_1 = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.
Title: {title}
Playwright: This is a synopsis for the above play:"""
PROMPT_TEMPLATE_2 = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.
Play Synopsis: {synopsis}
Review from a New York Times play critic of the above play:"""

INPUT_VARIABLES = {
    "input": "关于推动游戏设计边界的优秀视频游戏的纪录片"
}
```

```python
with Run(
    experiment_name=EXPERIMENT_NAME, run_name=RUN_NAME, sagemaker_session=session
) as run:
    # Create SageMaker Callback
    sagemaker_callback = SageMakerCallbackHandler(run)

    # Create prompt templates for the chain
    prompt_template1 = PromptTemplate.from_template(template=PROMPT_TEMPLATE_1)
    prompt_template2 = PromptTemplate.from_template(template=PROMPT_TEMPLATE_2)

    # Define LLM model with callback
    llm = OpenAI(callbacks=[sagemaker_callback], **HPARAMS)

    # Create chain1
    chain1 = LLMChain(llm=llm, prompt=prompt_template1, callbacks=[sagemaker_callback])

    # Create chain2
    chain2 = LLMChain(llm=llm, prompt=prompt_template2, callbacks=[sagemaker_callback])

    # Create Sequential chain
    overall_chain = SimpleSequentialChain(
        chains=[chain1, chain2], callbacks=[sagemaker_callback]
    )

    # Run overall sequential chain
    overall_chain.run(**INPUT_VARIABLES)

    # Reset the callback
    sagemaker_callback.flush_tracker()
```

### 场景 3 - 带工具的代理

```python
RUN_NAME = "run-scenario-3"
PROMPT_TEMPLATE = "谁是活着的最年长的人？他们当前的年龄提高到1.51的幂是多少？"
```

```python
with Run(
    experiment_name=EXPERIMENT_NAME, run_name=RUN_NAME, sagemaker_session=session
) as run:
    # 创建 SageMaker 回调
    sagemaker_callback = SageMakerCallbackHandler(run)

    # 定义带回调的 LLM 模型
    llm = OpenAI(callbacks=[sagemaker_callback], **HPARAMS)

    # 定义工具
    tools = load_tools(["serpapi", "llm-math"], llm=llm, callbacks=[sagemaker_callback])

    # 使用所有工具初始化代理
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", callbacks=[sagemaker_callback]
    )

    # 运行代理
    agent.run(input=PROMPT_TEMPLATE)

    # 重置回调
    sagemaker_callback.flush_tracker()
```

## 加载日志数据

一旦提示被记录，我们可以轻松地将其加载并转换为 Pandas DataFrame，如下所示。

```python
# Load
logs = ExperimentAnalytics(experiment_name=EXPERIMENT_NAME)

# Convert as pandas dataframe
df = logs.dataframe(force_refresh=True)

print(df.shape)
df.head()
```

如上所示，实验中有三次运行（行），对应于每个场景。每次运行记录了提示和相关的 LLM 设置/超参数，并以 json 格式保存到 s3 存储桶中。可以随意加载并探索每个 json 路径中的日志数据。