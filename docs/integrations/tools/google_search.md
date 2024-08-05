---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/google_search.ipynb
---

# Google搜索

此笔记本介绍了如何使用Google搜索组件。

首先，您需要设置正确的API密钥和环境变量。要进行设置，请在Google Cloud凭据控制台中创建GOOGLE_API_KEY（https://console.cloud.google.com/apis/credentials）和使用可编程搜索引擎创建GOOGLE_CSE_ID（https://programmablesearchengine.google.com/controlpanel/create）。接下来，建议遵循[这里](https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search)的说明。

然后，我们需要设置一些环境变量。

```python
%pip install --upgrade --quiet  langchain-community
```

```python
import os

os.environ["GOOGLE_CSE_ID"] = ""
os.environ["GOOGLE_API_KEY"] = ""
```

```python
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

search = GoogleSearchAPIWrapper()

tool = Tool(
    name="google_search",
    description="搜索Google以获取最新结果。",
    func=search.run,
)
```

```python
tool.run("Obama's first name?")
```

```output
"STATE OF HAWAII. 1 Child's First Name. (Type or print). 2. Sex. BARACK. 3. This Birth. CERTIFICATE OF LIVE BIRTH. FILE. NUMBER 151 le. lb. Middle Name. Barack Hussein Obama II is an American former politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic\xa0... When Barack Obama was elected president in 2008, he became the first African American to hold ... The Middle East remained a key foreign policy challenge. Jan 19, 2017 ... Jordan Barack Treasure, New York City, born in 2008 ... Jordan Barack Treasure made national news when he was the focus of a New York newspaper\xa0... Portrait of George Washington, the 1st President of the United States ... Portrait of Barack Obama, the 44th President of the United States\xa0... His full name is Barack Hussein Obama II. Since the “II” is simply because he was named for his father, his last name is Obama. Mar 22, 2008 ... Barry Obama decided that he didn't like his nickname. A few of his friends at Occidental College had already begun to call him Barack (his\xa0... Aug 18, 2017 ... It took him several seconds and multiple clues to remember former President Barack Obama's first name. Miller knew that every answer had to\xa0... Feb 9, 2015 ... Michael Jordan misspelled Barack Obama's first name on 50th-birthday gift ... Knowing Obama is a Chicagoan and huge basketball fan,\xa0... 4 days ago ... Barack Obama, in full Barack Hussein Obama II, (born August 4, 1961, Honolulu, Hawaii, U.S.), 44th president of the United States (2009–17) and\xa0..."
```

## 结果数量
您可以使用 `k` 参数来设置结果数量


```python
search = GoogleSearchAPIWrapper(k=1)

tool = Tool(
    name="I'm Feeling Lucky",
    description="Search Google and return the first result.",
    func=search.run,
)
```


```python
tool.run("python")
```



```output
'The official home of the Python Programming Language.'
```


'The official home of the Python Programming Language.'

## 元数据结果

通过 GoogleSearch 运行查询并返回片段、标题和链接元数据。

- 片段：结果的描述。
- 标题：结果的标题。
- 链接：结果的链接。


```python
search = GoogleSearchAPIWrapper()


def top5_results(query):
    return search.results(query, 5)


tool = Tool(
    name="Google Search Snippets",
    description="Search Google for recent results.",
    func=top5_results,
)
```

## 相关

- 工具 [概念指南](/docs/concepts/#tools)
- 工具 [操作指南](/docs/how_to/#tools)