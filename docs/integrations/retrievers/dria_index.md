---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/retrievers/dria_index.ipynb
---
# Dria

>[Dria](https://dria.co/) is a hub of public RAG models for developers to both contribute and utilize a shared embedding lake. This notebook demonstrates how to use the `Dria API` for data retrieval tasks.

# Installation

Ensure you have the `dria` package installed. You can install it using pip:


```python
%pip install --upgrade --quiet dria
```

# Configure API Key

Set up your Dria API key for access.


```python
import os

os.environ["DRIA_API_KEY"] = "DRIA_API_KEY"
```

# Initialize Dria Retriever

Create an instance of `DriaRetriever`.


```python
from langchain.retrievers import DriaRetriever

api_key = os.getenv("DRIA_API_KEY")
retriever = DriaRetriever(api_key=api_key)
```

# **Create Knowledge Base**

Create a knowledge on [Dria's Knowledge Hub](https://dria.co/knowledge)


```python
contract_id = retriever.create_knowledge_base(
    name="France's AI Development",
    embedding=DriaRetriever.models.jina_embeddings_v2_base_en.value,
    category="Artificial Intelligence",
    description="Explore the growth and contributions of France in the field of Artificial Intelligence.",
)
```

# Add Data

Load data into your Dria knowledge base.


```python
texts = [
    "The first text to add to Dria.",
    "Another piece of information to store.",
    "More data to include in the Dria knowledge base.",
]

ids = retriever.add_texts(texts)
print("Data added with IDs:", ids)
```

# Retrieve Data

Use the retriever to find relevant documents given a query.


```python
query = "Find information about Dria."
result = retriever.invoke(query)
for doc in result:
    print(doc)
```


## Related

- Retriever [conceptual guide](/docs/concepts/#retrievers)
- Retriever [how-to guides](/docs/how_to/#retrievers)