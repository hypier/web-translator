---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/kinetica.ipynb
sidebar_label: Kinetica
---
# Kinetica SqlAssist LLM Demo

This notebook demonstrates how to use Kinetica to transform natural language into SQL
and simplify the process of data retrieval. This demo is intended to show the mechanics
of creating and using a chain as opposed to the capabilities of the LLM.

## Overview

With the Kinetica LLM workflow you create an LLM context in the database that provides
information needed for infefencing that includes tables, annotations, rules, and
samples. Invoking ``ChatKinetica.load_messages_from_context()`` will retrieve the
context information from the database so that it can be used to create a chat prompt.

The chat prompt consists of a ``SystemMessage`` and pairs of
``HumanMessage``/``AIMessage`` that contain the samples which are question/SQL
pairs. You can append pairs samples to this list but it is not intended to
facilitate a typical natural language conversation.

When you create a chain from the chat prompt and execute it, the Kinetica LLM will
generate SQL from the input. Optionally you can use ``KineticaSqlOutputParser`` to
execute the SQL and return the result as a dataframe.

Currently, 2 LLM's are supported for SQL generation: 

1. **Kinetica SQL-GPT**: This LLM is based on OpenAI ChatGPT API.
2. **Kinetica SqlAssist**: This LLM is purpose built to integrate with the Kinetica
   database and it can run in a secure customer premise.

For this demo we will be using **SqlAssist**. See the [Kinetica Documentation
site](https://docs.kinetica.com/7.1/sql-gpt/concepts/) for more information.

## Prerequisites

To get started you will need a Kinetica DB instance. If you don't have one you can
obtain a [free development instance](https://cloud.kinetica.com/trynow).

You will need to install the following packages...


```python
# Install Langchain community and core packages
%pip install --upgrade --quiet langchain-core langchain-community

# Install Kineitca DB connection package
%pip install --upgrade --quiet 'gpudb>=7.2.0.8' typeguard pandas tqdm

# Install packages needed for this tutorial
%pip install --upgrade --quiet faker ipykernel 
```

## Database Connection

You must set the database connection in the following environment variables. If you are using a virtual environment you can set them in the `.env` file of the project:
* `KINETICA_URL`: Database connection URL
* `KINETICA_USER`: Database user
* `KINETICA_PASSWD`: Secure password.

If you can create an instance of `KineticaChatLLM` then you are successfully connected.


```python
from langchain_community.chat_models.kinetica import ChatKinetica

kinetica_llm = ChatKinetica()

# Test table we will create
table_name = "demo.user_profiles"

# LLM Context we will create
kinetica_ctx = "demo.test_llm_ctx"
```

## Create test data

Before we can generate SQL we will need to create a Kinetica table and an LLM context that can inference the table.

### Create some fake user profiles

We will use the `faker` package to create a dataframe with 100 fake profiles.


```python
from typing import Generator

import pandas as pd
from faker import Faker

Faker.seed(5467)
faker = Faker(locale="en-US")


def profile_gen(count: int) -> Generator:
    for id in range(0, count):
        rec = dict(id=id, **faker.simple_profile())
        rec["birthdate"] = pd.Timestamp(rec["birthdate"])
        yield rec


load_df = pd.DataFrame.from_records(data=profile_gen(100), index="id")
print(load_df.head())
```
```output
         username             name sex  \
id                                       
0       eduardo69       Haley Beck   F   
1        lbarrera  Joshua Stephens   M   
2         bburton     Paula Kaiser   F   
3       melissa49      Wendy Reese   F   
4   melissacarter      Manuel Rios   M   

                                              address                    mail  \
id                                                                              
0   59836 Carla Causeway Suite 939\nPort Eugene, I...  meltondenise@yahoo.com   
1   3108 Christina Forges\nPort Timothychester, KY...     erica80@hotmail.com   
2                    Unit 7405 Box 3052\nDPO AE 09858  timothypotts@gmail.com   
3   6408 Christopher Hill Apt. 459\nNew Benjamin, ...        dadams@gmail.com   
4    2241 Bell Gardens Suite 723\nScottside, CA 38463  williamayala@gmail.com   

    birthdate  
id             
0  1997-12-08  
1  1924-08-03  
2  1933-12-05  
3  1988-10-26  
4  1931-03-19
```
### Create a Kinetica table from the Dataframe


```python
from gpudb import GPUdbTable

gpudb_table = GPUdbTable.from_df(
    load_df,
    db=kinetica_llm.kdbc,
    table_name=table_name,
    clear_table=True,
    load_data=True,
)

# See the Kinetica column types
print(gpudb_table.type_as_df())
```
```output
        name    type   properties
0   username  string     [char32]
1       name  string     [char32]
2        sex  string      [char2]
3    address  string     [char64]
4       mail  string     [char32]
5  birthdate    long  [timestamp]
```
### Create the LLM context

You can create an LLM Context using the Kinetica Workbench UI or you can manually create it with the `CREATE OR REPLACE CONTEXT` syntax. 

Here we create a context from the SQL syntax referencing the table we created.


```python
from gpudb import GPUdbSamplesClause, GPUdbSqlContext, GPUdbTableClause

table_ctx = GPUdbTableClause(table=table_name, comment="Contains user profiles.")

samples_ctx = GPUdbSamplesClause(
    samples=[
        (
            "How many male users are there?",
            f"""
            select count(1) as num_users
                from {table_name}
                where sex = 'M';
            """,
        )
    ]
)

context_sql = GPUdbSqlContext(
    name=kinetica_ctx, tables=[table_ctx], samples=samples_ctx
).build_sql()

print(context_sql)
count_affected = kinetica_llm.kdbc.execute(context_sql)
count_affected
```
```output
CREATE OR REPLACE CONTEXT "demo"."test_llm_ctx" (
    TABLE = "demo"."user_profiles",
    COMMENT = 'Contains user profiles.'
),
(
    SAMPLES = ( 
        'How many male users are there?' = 'select count(1) as num_users
    from demo.user_profiles
    where sex = ''M'';' )
)
```


```output
1
```


## Use Langchain for inferencing

In the example below we will create a chain from the previously created table and LLM context. This chain will generate SQL and return the resulting data as a dataframe.

### Load the chat prompt from the Kinetica DB

The `load_messages_from_context()` function will retrieve a context from the DB and convert it into a list of chat messages that we use to create a ``ChatPromptTemplate``.


```python
from langchain_core.prompts import ChatPromptTemplate

# load the context from the database
ctx_messages = kinetica_llm.load_messages_from_context(kinetica_ctx)

# Add the input prompt. This is where input question will be substituted.
ctx_messages.append(("human", "{input}"))

# Create the prompt template.
prompt_template = ChatPromptTemplate.from_messages(ctx_messages)
prompt_template.pretty_print()
```
```output
================================[1m System Message [0m================================

CREATE TABLE demo.user_profiles AS
(
   username VARCHAR (32) NOT NULL,
   name VARCHAR (32) NOT NULL,
   sex VARCHAR (2) NOT NULL,
   address VARCHAR (64) NOT NULL,
   mail VARCHAR (32) NOT NULL,
   birthdate TIMESTAMP NOT NULL
);
COMMENT ON TABLE demo.user_profiles IS 'Contains user profiles.';

================================[1m Human Message [0m=================================

How many male users are there?

==================================[1m Ai Message [0m==================================

select count(1) as num_users
    from demo.user_profiles
    where sex = 'M';

================================[1m Human Message [0m=================================

[33;1m[1;3m{input}[0m
```
### Create the chain

The last element of this chain is `KineticaSqlOutputParser` that will execute the SQL and return a dataframe. This is optional and if we left it out then only SQL would be returned.


```python
from langchain_community.chat_models.kinetica import (
    KineticaSqlOutputParser,
    KineticaSqlResponse,
)

chain = prompt_template | kinetica_llm | KineticaSqlOutputParser(kdbc=kinetica_llm.kdbc)
```

### Generate the SQL

The chain we created will take a question as input and return a ``KineticaSqlResponse`` containing the generated SQL and data. The question must be relevant to the to LLM context we used to create the prompt.


```python
# Here you must ask a question relevant to the LLM context provided in the prompt template.
response: KineticaSqlResponse = chain.invoke(
    {"input": "What are the female users ordered by username?"}
)

print(f"SQL: {response.sql}")
print(response.dataframe.head())
```
```output
SQL: SELECT username, name
    FROM demo.user_profiles
    WHERE sex = 'F'
    ORDER BY username;
      username               name
0  alexander40       Tina Ramirez
1      bburton       Paula Kaiser
2      brian12  Stefanie Williams
3    brownanna      Jennifer Rowe
4       carl19       Amanda Potts
```

## Related

- Chat model [conceptual guide](/docs/concepts/#chat-models)
- Chat model [how-to guides](/docs/how_to/#chat-models)