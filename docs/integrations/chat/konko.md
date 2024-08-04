---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/konko.ipynb
sidebar_label: Konko
---
# ChatKonko

# Konko

>[Konko](https://www.konko.ai/) API is a fully managed Web API designed to help application developers:


1. **Select** the right open source or proprietary LLMs for their application
2. **Build** applications faster with integrations to leading application frameworks and fully managed APIs
3. **Fine tune** smaller open-source LLMs to achieve industry-leading performance at a fraction of the cost
4. **Deploy production-scale APIs** that meet security, privacy, throughput, and latency SLAs without infrastructure set-up or administration using Konko AI's SOC 2 compliant, multi-cloud infrastructure


This example goes over how to use LangChain to interact with `Konko` ChatCompletion [models](https://docs.konko.ai/docs/list-of-models#konko-hosted-models-for-chatcompletion)

To run this notebook, you'll need Konko API key. Sign in to our web app to [create an API key](https://platform.konko.ai/settings/api-keys) to access models




```python
from langchain_community.chat_models import ChatKonko
from langchain_core.messages import HumanMessage, SystemMessage
```

#### Set Environment Variables

1. You can set environment variables for 
   1. KONKO_API_KEY (Required)
   2. OPENAI_API_KEY (Optional)
2. In your current shell session, use the export command:

```shell
export KONKO_API_KEY={your_KONKO_API_KEY_here}
export OPENAI_API_KEY={your_OPENAI_API_KEY_here} #Optional
```

## Calling a model

Find a model on the [Konko overview page](https://docs.konko.ai/docs/list-of-models)

Another way to find the list of models running on the Konko instance is through this [endpoint](https://docs.konko.ai/reference/get-models).

From here, we can initialize our model:



```python
chat = ChatKonko(max_tokens=400, model="meta-llama/llama-2-13b-chat")
```


```python
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Explain Big Bang Theory briefly"),
]
chat(messages)
```



```output
AIMessage(content="  Sure thing! The Big Bang Theory is a scientific theory that explains the origins of the universe. In short, it suggests that the universe began as an infinitely hot and dense point around 13.8 billion years ago and expanded rapidly. This expansion continues to this day, and it's what makes the universe look the way it does.\n\nHere's a brief overview of the key points:\n\n1. The universe started as a singularity, a point of infinite density and temperature.\n2. The singularity expanded rapidly, causing the universe to cool and expand.\n3. As the universe expanded, particles began to form, including protons, neutrons, and electrons.\n4. These particles eventually came together to form atoms, and later, stars and galaxies.\n5. The universe is still expanding today, and the rate of this expansion is accelerating.\n\nThat's the Big Bang Theory in a nutshell! It's a pretty mind-blowing idea when you think about it, and it's supported by a lot of scientific evidence. Do you have any other questions about it?")
```



## Related

- Chat model [conceptual guide](/docs/concepts/#chat-models)
- Chat model [how-to guides](/docs/how_to/#chat-models)