---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/llms/huggingface_endpoint.ipynb
---
# Huggingface Endpoints

>The [Hugging Face Hub](https://huggingface.co/docs/hub/index) is a platform with over 120k models, 20k datasets, and 50k demo apps (Spaces), all open source and publicly available, in an online platform where people can easily collaborate and build ML together.

The `Hugging Face Hub` also offers various endpoints to build ML applications.
This example showcases how to connect to the different Endpoints types.

In particular, text generation inference is powered by [Text Generation Inference](https://github.com/huggingface/text-generation-inference): a custom-built Rust, Python and gRPC server for blazing-faset text generation inference.


```python
from langchain_huggingface import HuggingFaceEndpoint
```

## Installation and Setup

To use, you should have the ``huggingface_hub`` python [package installed](https://huggingface.co/docs/huggingface_hub/installation).


```python
%pip install --upgrade --quiet huggingface_hub
```


```python
# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token

from getpass import getpass

HUGGINGFACEHUB_API_TOKEN = getpass()
```


```python
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
```

## Prepare Examples


```python
from langchain_huggingface import HuggingFaceEndpoint
```


```python
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
```


```python
question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
```

## Examples

Here is an example of how you can access `HuggingFaceEndpoint` integration of the free [Serverless Endpoints](https://huggingface.co/inference-endpoints/serverless) API.


```python
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=128,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)
llm_chain = prompt | llm
print(llm_chain.invoke({"question": question}))
```

## Dedicated Endpoint


The free serverless API lets you implement solutions and iterate in no time, but it may be rate limited for heavy use cases, since the loads are shared with other requests.

For enterprise workloads, the best is to use [Inference Endpoints - Dedicated](https://huggingface.co/inference-endpoints/dedicated).
This gives access to a fully managed infrastructure that offer more flexibility and speed. These resoucres come with continuous support and uptime guarantees, as well as options like AutoScaling




```python
# Set the url to your Inference Endpoint below
your_endpoint_url = "https://fayjubiy2xqn36z0.us-east-1.aws.endpoints.huggingface.cloud"
```


```python
llm = HuggingFaceEndpoint(
    endpoint_url=f"{your_endpoint_url}",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)
llm("What did foo say about bar?")
```

### Streaming


```python
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    endpoint_url=f"{your_endpoint_url}",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
    streaming=True,
)
llm("What did foo say about bar?", callbacks=[StreamingStdOutCallbackHandler()])
```


## Related

- LLM [conceptual guide](/docs/concepts/#llms)
- LLM [how-to guides](/docs/how_to/#llms)