---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/vectorstores/zep_cloud.ipynb
---
# Zep Cloud
> Recall, understand, and extract data from chat histories. Power personalized AI experiences.

> [Zep](https://www.getzep.com) is a long-term memory service for AI Assistant apps.
> With Zep, you can provide AI assistants with the ability to recall past conversations, no matter how distant,
> while also reducing hallucinations, latency, and cost.

> See [Zep Cloud Installation Guide](https://help.getzep.com/sdks)

## Usage

In the examples below, we're using Zep's auto-embedding feature which automatically embeds documents on the Zep server 
using low-latency embedding models.

## Note
- These examples use Zep's async interfaces. Call sync interfaces by removing the `a` prefix from the method names.

## Load or create a Collection from documents


```python
from uuid import uuid4

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import ZepCloudVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

ZEP_API_KEY = "<your zep project key>"  # You can generate your zep project key from the Zep dashboard
collection_name = f"babbage{uuid4().hex}"  # a unique collection name. alphanum only

# load the document
article_url = "https://www.gutenberg.org/cache/epub/71292/pg71292.txt"
loader = WebBaseLoader(article_url)
documents = loader.load()

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Instantiate the VectorStore. Since the collection does not already exist in Zep,
# it will be created and populated with the documents we pass in.
vs = ZepCloudVectorStore.from_documents(
    docs,
    embedding=None,
    collection_name=collection_name,
    api_key=ZEP_API_KEY,
)
```


```python
# wait for the collection embedding to complete


async def wait_for_ready(collection_name: str) -> None:
    import time

    from zep_cloud.client import AsyncZep

    client = AsyncZep(api_key=ZEP_API_KEY)

    while True:
        c = await client.document.get_collection(collection_name)
        print(
            "Embedding status: "
            f"{c.document_embedded_count}/{c.document_count} documents embedded"
        )
        time.sleep(1)
        if c.document_embedded_count == c.document_count:
            break


await wait_for_ready(collection_name)
```
```output
Embedding status: 401/401 documents embedded
```
## Simarility Search Query over the Collection


```python
# query it
query = "what is the structure of our solar system?"
docs_scores = await vs.asimilarity_search_with_relevance_scores(query, k=3)

# print results
for d, s in docs_scores:
    print(d.page_content, " -> ", s, "\n====\n")
```
```output
the positions of the two principal planets, (and these the most
necessary for the navigator,) Jupiter and Saturn, require each not less
than one hundred and sixteen tables. Yet it is not only necessary to
predict the position of these bodies, but it is likewise expedient to
tabulate the motions of the four satellites of Jupiter, to predict the
exact times at which they enter his shadow, and at which their shadows
cross his disc, as well as the times at which they are interposed  ->  0.78691166639328 
====

are reduced to a system of wheel-work. We are, nevertheless, not without
hopes of conveying, even to readers unskilled in mathematics, some
satisfactory notions of a general nature on this subject.

_Thirdly_, To explain the actual state of the machinery at the present
time; what progress has been made towards its completion; and what are
the probable causes of those delays in its progress, which must be a
subject of regret to all friends of science. We shall indicate what  ->  0.7853284478187561 
====

from the improved state of astronomy, he found it necessary to recompute
these tables in 1821.

Although it is now about thirty years since the discovery of the four
new planets, Ceres, Pallas, Juno, and Vesta, it was not till recently
that tables of their motions were published. They have lately appeared
in Encke's Ephemeris.

We have thus attempted to convey some notion (though necessarily a very
inadequate one) of the immense extent of numerical tables which it has  ->  0.7840130925178528 
====
```
## Search over Collection Re-ranked by MMR

Zep offers native, hardware-accelerated MMR re-ranking of search results.


```python
query = "what is the structure of our solar system?"
docs = await vs.asearch(query, search_type="mmr", k=3)

for d in docs:
    print(d.page_content, "\n====\n")
```
```output
the positions of the two principal planets, (and these the most
necessary for the navigator,) Jupiter and Saturn, require each not less
than one hundred and sixteen tables. Yet it is not only necessary to
predict the position of these bodies, but it is likewise expedient to
tabulate the motions of the four satellites of Jupiter, to predict the
exact times at which they enter his shadow, and at which their shadows
cross his disc, as well as the times at which they are interposed 
====

are reduced to a system of wheel-work. We are, nevertheless, not without
hopes of conveying, even to readers unskilled in mathematics, some
satisfactory notions of a general nature on this subject.

_Thirdly_, To explain the actual state of the machinery at the present
time; what progress has been made towards its completion; and what are
the probable causes of those delays in its progress, which must be a
subject of regret to all friends of science. We shall indicate what 
====

general commerce. But the science in which, above all others, the most
extensive and accurate tables are indispensable, is Astronomy; with the
improvement and perfection of which is inseparably connected that of the
kindred art of Navigation. We scarcely dare hope to convey to the
general reader any thing approaching to an adequate notion of the
multiplicity and complexity of the tables necessary for the purposes of
the astronomer and navigator. We feel, nevertheless, that the truly 
====
```
# Filter by Metadata

Use a metadata filter to narrow down results. First, load another book: "Adventures of Sherlock Holmes"


```python
# Let's add more content to the existing Collection
article_url = "https://www.gutenberg.org/files/48320/48320-0.txt"
loader = WebBaseLoader(article_url)
documents = loader.load()

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

await vs.aadd_documents(docs)

await wait_for_ready(collection_name)
```

We see results from both books. Note the `source` metadata


```python
query = "Was he interested in astronomy?"
docs = await vs.asearch(query, search_type="similarity", k=3)

for d in docs:
    print(d.page_content, " -> ", d.metadata, "\n====\n")
```
```output
of astronomy, and its kindred sciences, with the various arts dependent
on them. In none are computations more operose than those which
astronomy in particular requires;--in none are preparatory facilities
more needful;--in none is error more detrimental. The practical
astronomer is interrupted in his pursuit, and diverted from his task of
observation by the irksome labours of computation, or his diligence in
observing becomes ineffectual for want of yet greater industry of  ->  {'source': 'https://www.gutenberg.org/cache/epub/71292/pg71292.txt'} 
====

possess all knowledge which is likely to be useful to him in his work,
and this I have endeavored in my case to do. If I remember rightly, you
on one occasion, in the early days of our friendship, defined my limits
in a very precise fashion.”

“Yes,” I answered, laughing. “It was a singular document. Philosophy,
astronomy, and politics were marked at zero, I remember. Botany
variable, geology profound as regards the mud-stains from any region  ->  {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'} 
====

easily admitted, that an assembly of eminent naturalists and physicians,
with a sprinkling of astronomers, and one or two abstract
mathematicians, were not precisely the persons best qualified to
appreciate such an instrument of mechanical investigation as we have
here described. We shall not therefore be understood as intending the
slightest disrespect for these distinguished persons, when we express
our regret, that a discovery of such paramount practical value, in a  ->  {'source': 'https://www.gutenberg.org/cache/epub/71292/pg71292.txt'} 
====
```
Now, we set up a filter


```python
filter = {
    "where": {
        "jsonpath": (
            "$[*] ? (@.source == 'https://www.gutenberg.org/files/48320/48320-0.txt')"
        )
    },
}

docs = await vs.asearch(query, search_type="similarity", metadata=filter, k=3)

for d in docs:
    print(d.page_content, " -> ", d.metadata, "\n====\n")
```
```output
possess all knowledge which is likely to be useful to him in his work,
and this I have endeavored in my case to do. If I remember rightly, you
on one occasion, in the early days of our friendship, defined my limits
in a very precise fashion.”

“Yes,” I answered, laughing. “It was a singular document. Philosophy,
astronomy, and politics were marked at zero, I remember. Botany
variable, geology profound as regards the mud-stains from any region  ->  {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'} 
====

the evening than in the daylight, for he said that he hated to be
conspicuous. Very retiring and gentlemanly he was. Even his voice was
gentle. He’d had the quinsy and swollen glands when he was young, he
told me, and it had left him with a weak throat, and a hesitating,
whispering fashion of speech. He was always well dressed, very neat and
plain, but his eyes were weak, just as mine are, and he wore tinted
glasses against the glare.”  ->  {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'} 
====

which was characteristic of him. “It is perhaps less suggestive than
it might have been,” he remarked, “and yet there are a few inferences
which are very distinct, and a few others which represent at least a
strong balance of probability. That the man was highly intellectual
is of course obvious upon the face of it, and also that he was fairly
well-to-do within the last three years, although he has now fallen upon
evil days. He had foresight, but has less now than formerly, pointing  ->  {'source': 'https://www.gutenberg.org/files/48320/48320-0.txt'} 
====
```

## Related

- Vector store [conceptual guide](/docs/concepts/#vector-stores)
- Vector store [how-to guides](/docs/how_to/#vector-stores)
