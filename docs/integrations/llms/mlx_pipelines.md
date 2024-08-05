---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/llms/mlx_pipelines.ipynb
---

# MLX 本地管道

MLX 模型可以通过 `MLXPipeline` 类在本地运行。

[MLX 社区](https://huggingface.co/mlx-community) 托管了超过 150 个模型，所有模型都是开源的，并且可以在 Hugging Face Model Hub 上公开获取，这是一个人们可以轻松协作并共同构建机器学习的平台。

这些模型可以通过 LangChain 调用，既可以通过这个本地管道包装器，也可以通过 MlXPipeline 类调用它们的托管推理端点。有关 mlx 的更多信息，请参见 [示例库](https://github.com/ml-explore/mlx-examples/tree/main/llms) 笔记本。

要使用它，您需要安装 ``mlx-lm`` python [包](https://pypi.org/project/mlx-lm/)，以及 [transformers](https://pypi.org/project/transformers/)。您还可以安装 `huggingface_hub`。

```python
%pip install --upgrade --quiet  mlx-lm transformers huggingface_hub
```

### 模型加载

可以通过使用 `from_model_id` 方法指定模型参数来加载模型。

```python
from langchain_community.llms.mlx_pipeline import MLXPipeline

pipe = MLXPipeline.from_model_id(
    "mlx-community/quantized-gemma-2b-it",
    pipeline_kwargs={"max_tokens": 10, "temp": 0.1},
)
```

也可以通过直接传入现有的 `transformers` 管道来加载模型。

```python
from mlx_lm import load

model, tokenizer = load("mlx-community/quantized-gemma-2b-it")
pipe = MLXPipeline(model=model, tokenizer=tokenizer)
```

### 创建链

模型加载到内存后，您可以通过提示将其组合形成链。

```python
from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | pipe

question = "What is electroencephalography?"

print(chain.invoke({"question": question}))
```

## 相关

- LLM [概念指南](/docs/concepts/#llms)
- LLM [操作指南](/docs/how_to/#llms)