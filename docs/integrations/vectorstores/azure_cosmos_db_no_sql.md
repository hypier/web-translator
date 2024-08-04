---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/vectorstores/azure_cosmos_db_no_sql.ipynb
---
# Azure Cosmos DB No SQL

This notebook shows you how to leverage this integrated [vector database](https://learn.microsoft.com/en-us/azure/cosmos-db/vector-database) to store documents in collections, create indicies and perform vector search queries using approximate nearest neighbor algorithms such as COS (cosine distance), L2 (Euclidean distance), and IP (inner product) to locate documents close to the query vectors. 
    
Azure Cosmos DB is the database that powers OpenAI's ChatGPT service. It offers single-digit millisecond response times, automatic and instant scalability, along with guaranteed speed at any scale. 

[Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search) now offers vector indexing and search in preview. This feature is designed to handle high-dimensional vectors, enabling efficient and accurate vector search at any scale. You can now store vectors directly in the documents alongside your data. This means that each document in your database can contain not only traditional schema-free data, but also high-dimensional vectors as other properties of the documents. This colocation of data and vectors allows for efficient indexing and searching, as the vectors are stored in the same logical unit as the data they represent. This simplifies data management, AI application architectures, and the efficiency of vector-based operations.

[Sign Up](https://azure.microsoft.com/en-us/free/) for lifetime free access to get started today.


```python
%pip install --upgrade --quiet azure-cosmos langchain-openai langchain-community
```
```output
Note: you may need to restart the kernel to use updated packages.
```

```python
OPENAI_API_KEY = "YOUR_KEY"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2023-05-15"
OPENAI_API_BASE = "YOUR_ENDPOINT"
OPENAI_EMBEDDINGS_MODEL_NAME = "text-embedding-ada-002"
OPENAI_EMBEDDINGS_MODEL_DEPLOYMENT = "text-embedding-ada-002"
```

## Insert Data


```python
from langchain_community.document_loaders import PyPDFLoader

# Load the PDF
loader = PyPDFLoader("https://arxiv.org/pdf/2303.08774.pdf")
data = loader.load()
```


```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)
```


```python
print(docs[0])
```
```output
page_content='GPT-4 Technical Report\nOpenAI∗\nAbstract\nWe report the development of GPT-4, a large-scale, multimodal model which can\naccept image and text inputs and produce text outputs. While less capable than\nhumans in many real-world scenarios, GPT-4 exhibits human-level performance\non various professional and academic benchmarks, including passing a simulated\nbar exam with a score around the top 10% of test takers. GPT-4 is a Transformer-\nbased model pre-trained to predict the next token in a document. The post-training\nalignment process results in improved performance on measures of factuality and\nadherence to desired behavior. A core component of this project was developing\ninfrastructure and optimization methods that behave predictably across a wide\nrange of scales. This allowed us to accurately predict some aspects of GPT-4’s\nperformance based on models trained with no more than 1/1,000th the compute of\nGPT-4.\n1 Introduction' metadata={'source': 'https://arxiv.org/pdf/2303.08774.pdf', 'page': 0}
```
## Creating AzureCosmosDB NoSQL Vector Search


```python
indexing_policy = {
    "indexingMode": "consistent",
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": '/"_etag"/?'}],
    "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
}

vector_embedding_policy = {
    "vectorEmbeddings": [
        {
            "path": "/embedding",
            "dataType": "float32",
            "distanceFunction": "cosine",
            "dimensions": 1536,
        }
    ]
}
```


```python
from azure.cosmos import CosmosClient, PartitionKey
from langchain_community.vectorstores.azure_cosmos_db_no_sql import (
    AzureCosmosDBNoSqlVectorSearch,
)
from langchain_openai import AzureOpenAIEmbeddings

HOST = "AZURE_COSMOS_DB_ENDPOINT"
KEY = "AZURE_COSMOS_DB_KEY"

cosmos_client = CosmosClient(HOST, KEY)
database_name = "langchain_python_db"
container_name = "langchain_python_container"
partition_key = PartitionKey(path="/id")
cosmos_container_properties = {"partition_key": partition_key}

openai_embeddings = AzureOpenAIEmbeddings(
    azure_deployment=OPENAI_EMBEDDINGS_MODEL_DEPLOYMENT,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
)

# insert the documents in AzureCosmosDBNoSql with their embedding
vector_search = AzureCosmosDBNoSqlVectorSearch.from_documents(
    documents=docs,
    embedding=openai_embeddings,
    cosmos_client=cosmos_client,
    database_name=database_name,
    container_name=container_name,
    vector_embedding_policy=vector_embedding_policy,
    indexing_policy=indexing_policy,
    cosmos_container_properties=cosmos_container_properties,
)
```

## Querying Data


```python
# Perform a similarity search between the embedding of the query and the embeddings of the documents
query = "What were the compute requirements for training GPT 4"
results = vector_search.similarity_search(query)

print(results[0].page_content)
```
```output
performance based on models trained with no more than 1/1,000th the compute of
GPT-4.
1 Introduction
This technical report presents GPT-4, a large multimodal model capable of processing image and
text inputs and producing text outputs. Such models are an important area of study as they have the
potential to be used in a wide range of applications, such as dialogue systems, text summarization,
and machine translation. As such, they have been the subject of substantial interest and progress in
recent years [1–34].
One of the main goals of developing such models is to improve their ability to understand and generate
natural language text, particularly in more complex and nuanced scenarios. To test its capabilities
in such scenarios, GPT-4 was evaluated on a variety of exams originally designed for humans. In
these evaluations it performs quite well and often outscores the vast majority of human test takers.
```
## Similarity Search with Score


```python
query = "What were the compute requirements for training GPT 4"

results = vector_search.similarity_search_with_score(
    query=query,
    k=5,
)

# Display results
for result in results:
    print(result)
```


## Related

- Vector store [conceptual guide](/docs/concepts/#vector-stores)
- Vector store [how-to guides](/docs/how_to/#vector-stores)
