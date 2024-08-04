---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/how_to/add_scores_retriever.ipynb
---

# 如何为检索结果添加分数

检索器将返回[Document](https://api.python.langchain.com/en/latest/documents/langchain_core.documents.base.Document.html)对象的序列，这些对象默认不包含有关检索过程的信息（例如，与查询的相似度分数）。在这里，我们演示如何将检索分数添加到文档的`.metadata`中：
1. 从[vectorstore retrievers](/docs/how_to/vectorstore_retriever);
2. 从更高阶的LangChain检索器，例如[SelfQueryRetriever](/docs/how_to/self_query)或[MultiVectorRetriever](/docs/how_to/multi_vector).

对于（1），我们将围绕相应的向量存储实现一个简短的包装函数。对于（2），我们将更新相应类的方法。

## 创建向量存储

首先，我们用一些数据填充向量存储。我们将使用 [PineconeVectorStore](https://api.python.langchain.com/en/latest/vectorstores/langchain_pinecone.vectorstores.PineconeVectorStore.html)，但本指南与任何实现 `.similarity_search_with_score` 方法的 LangChain 向量存储兼容。

```python
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"},
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={"year": 2010, "director": "Christopher Nolan", "rating": 8.2},
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6},
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3},
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={"year": 1995, "genre": "animated"},
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={
            "year": 1979,
            "director": "Andrei Tarkovsky",
            "genre": "thriller",
            "rating": 9.9,
        },
    ),
]

vectorstore = PineconeVectorStore.from_documents(
    docs, index_name="sample", embedding=OpenAIEmbeddings()
)
```

## 检索器

为了从向量存储检索器中获取分数，我们将底层向量存储的 `.similarity_search_with_score` 方法封装在一个短函数中，该函数将分数打包到相关文档的元数据中。

我们为该函数添加了一个 `@chain` 装饰器，以创建一个可以类似于典型检索器使用的 [Runnable](/docs/concepts/#langchain-expression-language)。

```python
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain


@chain
def retriever(query: str) -> List[Document]:
    docs, scores = zip(*vectorstore.similarity_search_with_score(query))
    for doc, score in zip(docs, scores):
        doc.metadata["score"] = score

    return docs
```


```python
result = retriever.invoke("dinosaur")
result
```



```output
(Document(page_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'genre': 'science fiction', 'rating': 7.7, 'year': 1993.0, 'score': 0.84429127}),
 Document(page_content='Toys come alive and have a blast doing so', metadata={'genre': 'animated', 'year': 1995.0, 'score': 0.792038262}),
 Document(page_content='Three men walk into the Zone, three men walk out of the Zone', metadata={'director': 'Andrei Tarkovsky', 'genre': 'thriller', 'rating': 9.9, 'year': 1979.0, 'score': 0.751571238}),
 Document(page_content='A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea', metadata={'director': 'Satoshi Kon', 'rating': 8.6, 'year': 2006.0, 'score': 0.747471571}))
```


请注意，从检索步骤获得的相似性分数包含在上述文档的元数据中。

## SelfQueryRetriever

`SelfQueryRetriever` 将使用 LLM 生成一个可能结构化的查询——例如，它可以在通常基于语义相似性选择的基础上构建检索过滤器。有关更多详细信息，请参见 [本指南](/docs/how_to/self_query)。

`SelfQueryRetriever` 包含一个简短的方法 `_get_docs_with_query`（1 - 2 行），该方法执行 `vectorstore` 搜索。我们可以子类化 `SelfQueryRetriever` 并重写此方法以传播相似性分数。

首先，按照 [如何指南](/docs/how_to/self_query)，我们需要建立一些用于过滤的元数据：

```python
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI

metadata_field_info = [
    AttributeInfo(
        name="genre",
        description="电影的类型。可选值包括 ['science fiction', 'comedy', 'drama', 'thriller', 'romance', 'action', 'animated']",
        type="string",
    ),
    AttributeInfo(
        name="year",
        description="电影上映的年份",
        type="integer",
    ),
    AttributeInfo(
        name="director",
        description="电影导演的名字",
        type="string",
    ),
    AttributeInfo(
        name="rating", description="电影的评分，范围为 1-10", type="float"
    ),
]
document_content_description = "电影的简要总结"
llm = ChatOpenAI(temperature=0)
```

然后我们重写 `_get_docs_with_query` 方法，以使用底层向量存储的 `similarity_search_with_score` 方法：

```python
from typing import Any, Dict


class CustomSelfQueryRetriever(SelfQueryRetriever):
    def _get_docs_with_query(
        self, query: str, search_kwargs: Dict[str, Any]
    ) -> List[Document]:
        """获取文档，并添加分数信息。"""
        docs, scores = zip(
            *vectorstore.similarity_search_with_score(query, **search_kwargs)
        )
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = score

        return docs
```

调用此检索器现在将在文档元数据中包含相似性分数。请注意，`SelfQueryRetriever` 的底层结构化查询功能得以保留。

```python
retriever = CustomSelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
)


result = retriever.invoke("dinosaur movie with rating less than 8")
result
```

```output
(Document(page_content='A bunch of scientists bring back dinosaurs and mayhem breaks loose', metadata={'genre': 'science fiction', 'rating': 7.7, 'year': 1993.0, 'score': 0.84429127}),)
```

## MultiVectorRetriever

`MultiVectorRetriever` 允许您将多个向量与单个文档关联。这在许多应用中都很有用。例如，我们可以对较大文档的小块进行索引，并在这些块上运行检索，但在调用检索器时返回较大的“父”文档。[ParentDocumentRetriever](/docs/how_to/parent_document_retriever/) 是 `MultiVectorRetriever` 的一个子类，包含填充向量存储以支持此功能的便利方法。更多应用详见此 [使用指南](/docs/how_to/multi_vector/)。

为了通过此检索器传播相似度分数，我们可以再次子类化 `MultiVectorRetriever` 并重写一个方法。这次我们将重写 `_get_relevant_documents`。

首先，我们准备一些虚假数据。我们生成虚假的“完整文档”，并将其存储在文档存储中；这里我们将使用一个简单的 [InMemoryStore](https://api.python.langchain.com/en/latest/stores/langchain_core.stores.InMemoryBaseStore.html)。

```python
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# The storage layer for the parent documents
docstore = InMemoryStore()
fake_whole_documents = [
    ("fake_id_1", Document(page_content="fake whole document 1")),
    ("fake_id_2", Document(page_content="fake whole document 2")),
]
docstore.mset(fake_whole_documents)
```

接下来，我们将向向量存储中添加一些虚假的“子文档”。我们可以通过填充其元数据中的 `"doc_id"` 键来将这些子文档链接到父文档。

```python
docs = [
    Document(
        page_content="A snippet from a larger document discussing cats.",
        metadata={"doc_id": "fake_id_1"},
    ),
    Document(
        page_content="A snippet from a larger document discussing discourse.",
        metadata={"doc_id": "fake_id_1"},
    ),
    Document(
        page_content="A snippet from a larger document discussing chocolate.",
        metadata={"doc_id": "fake_id_2"},
    ),
]

vectorstore.add_documents(docs)
```

```output
['62a85353-41ff-4346-bff7-be6c8ec2ed89',
 '5d4a0e83-4cc5-40f1-bc73-ed9cbad0ee15',
 '8c1d9a56-120f-45e4-ba70-a19cd19a38f4']
```

为了传播分数，我们子类化 `MultiVectorRetriever` 并重写其 `_get_relevant_documents` 方法。在这里我们将进行两个更改：

1. 我们将使用底层向量存储的 `similarity_search_with_score` 方法将相似度分数添加到相应“子文档”的元数据中；
2. 我们将在检索到的父文档的元数据中包含这些子文档的列表。这显示了通过检索识别出的文本片段及其相应的相似度分数。

```python
from collections import defaultdict

from langchain.retrievers import MultiVectorRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun


class CustomMultiVectorRetriever(MultiVectorRetriever):
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get documents relevant to a query.
        Args:
            query: String to find relevant documents for
            run_manager: The callbacks handler to use
        Returns:
            List of relevant documents
        """
        results = self.vectorstore.similarity_search_with_score(
            query, **self.search_kwargs
        )

        # Map doc_ids to list of sub-documents, adding scores to metadata
        id_to_doc = defaultdict(list)
        for doc, score in results:
            doc_id = doc.metadata.get("doc_id")
            if doc_id:
                doc.metadata["score"] = score
                id_to_doc[doc_id].append(doc)

        # Fetch documents corresponding to doc_ids, retaining sub_docs in metadata
        docs = []
        for _id, sub_docs in id_to_doc.items():
            docstore_docs = self.docstore.mget([_id])
            if docstore_docs:
                if doc := docstore_docs[0]:
                    doc.metadata["sub_docs"] = sub_docs
                    docs.append(doc)

        return docs
```

调用此检索器，我们可以看到它识别了正确的父文档，包括来自子文档的相关片段及其相似度分数。

```python
retriever = CustomMultiVectorRetriever(vectorstore=vectorstore, docstore=docstore)

retriever.invoke("cat")
```

```output
[Document(page_content='fake whole document 1', metadata={'sub_docs': [Document(page_content='A snippet from a larger document discussing cats.', metadata={'doc_id': 'fake_id_1', 'score': 0.831276655})]})]
```