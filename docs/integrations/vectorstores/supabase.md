---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/vectorstores/supabase.ipynb
---
# Supabase (Postgres)

>[Supabase](https://supabase.com/docs) is an open-source Firebase alternative. `Supabase` is built on top of `PostgreSQL`, which offers strong SQL querying capabilities and enables a simple interface with already-existing tools and frameworks.

>[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) also known as `Postgres`, is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

This notebook shows how to use `Supabase` and `pgvector` as your VectorStore.

You'll need to install `langchain-community` with `pip install -qU langchain-community` to use this integration

To run this notebook, please ensure:
- the `pgvector` extension is enabled
- you have installed the `supabase-py` package
- that you have created a `match_documents` function in your database
- that you have a `documents` table in your `public` schema similar to the one below.

The following function determines cosine similarity, but you can adjust to your needs.

```sql
-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table
  documents (
    id uuid primary key,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed
  );

-- Create a function to search for documents
create function match_documents (
  query_embedding vector (1536),
  filter jsonb default '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding;
end;
$$;
```


```python
# with pip
%pip install --upgrade --quiet  supabase

# with conda
# !conda install -c conda-forge supabase
```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
os.environ["SUPABASE_URL"] = getpass.getpass("Supabase URL:")
```


```python
os.environ["SUPABASE_SERVICE_KEY"] = getpass.getpass("Supabase Service Key:")
```


```python
# If you're storing your Supabase and OpenAI API keys in a .env file, you can load them with dotenv
from dotenv import load_dotenv

load_dotenv()
```

First we'll create a Supabase client and instantiate a OpenAI embeddings class.


```python
import os

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings()
```

Next we'll load and parse some data for our vector store (skip if you already have documents with embeddings stored in your DB).


```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

loader = TextLoader("../../how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

Insert the above documents into the database. Embeddings will automatically be generated for each document. You can adjust the chunk_size based on the amount of documents you have. The default is 500 but lowering it may be necessary.


```python
vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
    chunk_size=500,
)
```

Alternatively if you already have documents with embeddings in your database, simply instantiate a new `SupabaseVectorStore` directly:


```python
vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)
```

Finally, test it out by performing a similarity search:


```python
query = "What did the president say about Ketanji Brown Jackson"
matched_docs = vector_store.similarity_search(query)
```


```python
print(matched_docs[0].page_content)
```
```output
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
```
## Similarity search with score


The returned distance score is cosine distance. Therefore, a lower score is better.


```python
matched_docs = vector_store.similarity_search_with_relevance_scores(query)
```


```python
matched_docs[0]
```



```output
(Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'}),
 0.802509746274066)
```


## Retriever options

This section goes over different options for how to use SupabaseVectorStore as a retriever.

### Maximal Marginal Relevance Searches

In addition to using similarity search in the retriever object, you can also use `mmr`.



```python
retriever = vector_store.as_retriever(search_type="mmr")
```


```python
matched_docs = retriever.invoke(query)
```


```python
for i, d in enumerate(matched_docs):
    print(f"\n## Document {i}\n")
    print(d.page_content)
```


## Related

- Vector store [conceptual guide](/docs/concepts/#vector-stores)
- Vector store [how-to guides](/docs/how_to/#vector-stores)
