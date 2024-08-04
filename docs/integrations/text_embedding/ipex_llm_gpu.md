---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/text_embedding/ipex_llm_gpu.ipynb
---
# Local BGE Embeddings with IPEX-LLM on Intel GPU

> [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency.

This example goes over how to use LangChain to conduct embedding tasks with `ipex-llm` optimizations on Intel GPU. This would be helpful in applications such as RAG, document QA, etc.

> **Note**
>
> It is recommended that only Windows users with Intel Arc A-Series GPU (except for Intel Arc A300-Series or Pro A60) run this Jupyter notebook directly. For other cases (e.g. Linux users, Intel iGPU, etc.), it is recommended to run the code with Python scripts in terminal for best experiences.

## Install Prerequisites
To benefit from IPEX-LLM on Intel GPUs, there are several prerequisite steps for tools installation and environment preparation.

If you are a Windows user, visit the [Install IPEX-LLM on Windows with Intel GPU Guide](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html), and follow [Install Prerequisites](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html#install-prerequisites) to update GPU driver (optional) and install Conda.

If you are a Linux user, visit the [Install IPEX-LLM on Linux with Intel GPU](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html), and follow [**Install Prerequisites**](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#install-prerequisites) to install GPU driver, Intel® oneAPI Base Toolkit 2024.0, and Conda.

## Setup

After the prerequisites installation, you should have created a conda environment with all prerequisites installed. **Start the jupyter service in this conda environment**:


```python
%pip install -qU langchain langchain-community
```

Install IPEX-LLM for optimizations on Intel GPU, as well as `sentence-transformers`.


```python
%pip install --pre --upgrade ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
%pip install sentence-transformers
```

> **Note**
>
> You can also use `https://pytorch-extension.intel.com/release-whl/stable/xpu/cn/` as the extra-indel-url.

## Runtime Configuration

For optimal performance, it is recommended to set several environment variables based on your device:

### For Windows Users with Intel Core Ultra integrated GPU


```python
import os

os.environ["SYCL_CACHE_PERSISTENT"] = "1"
os.environ["BIGDL_LLM_XMX_DISABLED"] = "1"
```

### For Windows Users with Intel Arc A-Series GPU


```python
import os

os.environ["SYCL_CACHE_PERSISTENT"] = "1"
```

> **Note**
>
> For the first time that each model runs on Intel iGPU/Intel Arc A300-Series or Pro A60, it may take several minutes to compile.
>
> For other GPU type, please refer to [here](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#runtime-configuration) for Windows users, and  [here](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#id5) for Linux users.


## Basic Usage

Setting `device` to `"xpu"` in `model_kwargs` when initializing `IpexLLMBgeEmbeddings` will put the embedding model on Intel GPU and benefit from IPEX-LLM optimizations:


```python
from langchain_community.embeddings import IpexLLMBgeEmbeddings

embedding_model = IpexLLMBgeEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "xpu"},
    encode_kwargs={"normalize_embeddings": True},
)
```

API Reference
- [IpexLLMBgeEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.ipex_llm.IpexLLMBgeEmbeddings.html)


```python
sentence = "IPEX-LLM is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency."
query = "What is IPEX-LLM?"

text_embeddings = embedding_model.embed_documents([sentence, query])
print(f"text_embeddings[0][:10]: {text_embeddings[0][:10]}")
print(f"text_embeddings[1][:10]: {text_embeddings[1][:10]}")

query_embedding = embedding_model.embed_query(query)
print(f"query_embedding[:10]: {query_embedding[:10]}")
```


## Related

- Embedding model [conceptual guide](/docs/concepts/#embedding-models)
- Embedding model [how-to guides](/docs/how_to/#embedding-models)