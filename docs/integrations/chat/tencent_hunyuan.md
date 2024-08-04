---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/tencent_hunyuan.ipynb
sidebar_label: Tencent Hunyuan
---
# Tencent Hunyuan

>[Tencent's hybrid model API](https://cloud.tencent.com/document/product/1729) (`Hunyuan API`) 
> implements dialogue communication, content generation, 
> analysis and understanding, and can be widely used in various scenarios such as intelligent 
> customer service, intelligent marketing, role playing, advertising copywriting, product description,
> script creation, resume generation, article writing, code generation, data analysis, and content
> analysis.

See for [more information](https://cloud.tencent.com/document/product/1729).


```python
from langchain_community.chat_models import ChatHunyuan
from langchain_core.messages import HumanMessage
```


```python
chat = ChatHunyuan(
    hunyuan_app_id=111111111,
    hunyuan_secret_id="YOUR_SECRET_ID",
    hunyuan_secret_key="YOUR_SECRET_KEY",
)
```


```python
chat(
    [
        HumanMessage(
            content="You are a helpful assistant that translates English to French.Translate this sentence from English to French. I love programming."
        )
    ]
)
```



```output
AIMessage(content="J'aime programmer.")
```


## For ChatHunyuan with Streaming


```python
chat = ChatHunyuan(
    hunyuan_app_id="YOUR_APP_ID",
    hunyuan_secret_id="YOUR_SECRET_ID",
    hunyuan_secret_key="YOUR_SECRET_KEY",
    streaming=True,
)
```


```python
chat(
    [
        HumanMessage(
            content="You are a helpful assistant that translates English to French.Translate this sentence from English to French. I love programming."
        )
    ]
)
```



```output
AIMessageChunk(content="J'aime programmer.")
```



## Related

- Chat model [conceptual guide](/docs/concepts/#chat-models)
- Chat model [how-to guides](/docs/how_to/#chat-models)