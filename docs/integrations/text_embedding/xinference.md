---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/text_embedding/xinference.ipynb
---
# Xorbits inference (Xinference)

This notebook goes over how to use Xinference embeddings within LangChain

## Installation

Install `Xinference` through PyPI:


```python
%pip install --upgrade --quiet  "xinference[all]"
```

## Deploy Xinference Locally or in a Distributed Cluster.

For local deployment, run `xinference`. 

To deploy Xinference in a cluster, first start an Xinference supervisor using the `xinference-supervisor`. You can also use the option -p to specify the port and -H to specify the host. The default port is 9997.

Then, start the Xinference workers using `xinference-worker` on each server you want to run them on. 

You can consult the README file from [Xinference](https://github.com/xorbitsai/inference) for more information.

## Wrapper

To use Xinference with LangChain, you need to first launch a model. You can use command line interface (CLI) to do so:


```python
!xinference launch -n vicuna-v1.3 -f ggmlv3 -q q4_0
```
```output
Model uid: 915845ee-2a04-11ee-8ed4-d29396a3f064
```
A model UID is returned for you to use. Now you can use Xinference embeddings with LangChain:


```python
from langchain_community.embeddings import XinferenceEmbeddings

xinference = XinferenceEmbeddings(
    server_url="http://0.0.0.0:9997", model_uid="915845ee-2a04-11ee-8ed4-d29396a3f064"
)
```


```python
query_result = xinference.embed_query("This is a test query")
```


```python
doc_result = xinference.embed_documents(["text A", "text B"])
```

Lastly, terminate the model when you do not need to use it:


```python
!xinference terminate --model-uid "915845ee-2a04-11ee-8ed4-d29396a3f064"
```


## Related

- Embedding model [conceptual guide](/docs/concepts/#embedding-models)
- Embedding model [how-to guides](/docs/how_to/#embedding-models)