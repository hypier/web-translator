---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/wikipedia.ipynb
---
# Wikipedia

>[Wikipedia](https://wikipedia.org/) is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians, through open collaboration and using a wiki-based editing system called MediaWiki. `Wikipedia` is the largest and most-read reference work in history.

First, you need to install `wikipedia` python package.


```python
%pip install --upgrade --quiet  wikipedia
```


```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
```


```python
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
```


```python
wikipedia.run("HUNTER X HUNTER")
```





## Related

- Tool [conceptual guide](/docs/concepts/#tools)
- Tool [how-to guides](/docs/how_to/#tools)
