---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/chat/kinetica.ipynb
sidebar_label: Kinetica
---

# Kinetica SqlAssist LLM 演示

本笔记本演示了如何使用 Kinetica 将自然语言转换为 SQL，并简化数据检索的过程。此演示旨在展示创建和使用链的机制，而不是 LLM 的能力。

## 概述

通过 Kinetica LLM 工作流，您可以在数据库中创建一个 LLM 上下文，该上下文提供进行推理所需的信息，包括表格、注释、规则和示例。调用 ``ChatKinetica.load_messages_from_context()`` 将从数据库中检索上下文信息，以便用于创建聊天提示。

聊天提示由 ``SystemMessage`` 和包含样本的 ``HumanMessage``/``AIMessage`` 对组成，这些样本是问题/SQL 对。您可以将样本对附加到此列表中，但这并不旨在促进典型的自然语言对话。

当您从聊天提示创建一个链并执行时，Kinetica LLM 将根据输入生成 SQL。您可以选择使用 ``KineticaSqlOutputParser`` 来执行 SQL 并将结果以数据框的形式返回。

目前，支持用于 SQL 生成的 2 个 LLM：

1. **Kinetica SQL-GPT**：该 LLM 基于 OpenAI ChatGPT API。
2. **Kinetica SqlAssist**：该 LLM 是专门构建的，可以与 Kinetica 数据库集成，并且可以在安全的客户环境中运行。

在本演示中，我们将使用 **SqlAssist**。有关更多信息，请参见 [Kinetica 文档网站](https://docs.kinetica.com/7.1/sql-gpt/concepts/)。

## 前提条件

要开始，您需要一个 Kinetica DB 实例。如果您没有，可以获得一个 [免费的开发实例](https://cloud.kinetica.com/trynow)。

您需要安装以下软件包...

```python
# Install Langchain community and core packages
%pip install --upgrade --quiet langchain-core langchain-community

# Install Kineitca DB connection package
%pip install --upgrade --quiet 'gpudb>=7.2.0.8' typeguard pandas tqdm

# Install packages needed for this tutorial
%pip install --upgrade --quiet faker ipykernel 
```

## 数据库连接

您必须在以下环境变量中设置数据库连接。如果您使用虚拟环境，可以在项目的 `.env` 文件中设置它们：
* `KINETICA_URL`: 数据库连接 URL
* `KINETICA_USER`: 数据库用户
* `KINETICA_PASSWD`: 安全密码。

如果您可以创建 `KineticaChatLLM` 的实例，那么您已经成功连接。


```python
from langchain_community.chat_models.kinetica import ChatKinetica

kinetica_llm = ChatKinetica()

# Test table we will create
table_name = "demo.user_profiles"

# LLM Context we will create
kinetica_ctx = "demo.test_llm_ctx"
```

## 创建测试数据

在生成 SQL 之前，我们需要创建一个 Kinetica 表和一个可以推断该表的 LLM 上下文。

### 创建一些虚假用户档案

我们将使用 `faker` 包创建一个包含 100 个虚假档案的数据框。

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

### 从 Dataframe 创建 Kinetica 表

```python
from gpudb import GPUdbTable

gpudb_table = GPUdbTable.from_df(
    load_df,
    db=kinetica_llm.kdbc,
    table_name=table_name,
    clear_table=True,
    load_data=True,
)

# 查看 Kinetica 列类型
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

### 创建 LLM 上下文

您可以使用 Kinetica Workbench UI 创建 LLM 上下文，或者可以使用 `CREATE OR REPLACE CONTEXT` 语法手动创建它。

在这里，我们从 SQL 语法创建一个上下文，引用我们创建的表。

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

## 使用 Langchain 进行推理

在下面的示例中，我们将从之前创建的表和 LLM 上下文中创建一个链。这个链将生成 SQL 并将结果数据作为数据框返回。

### 从 Kinetica DB 加载聊天提示

`load_messages_from_context()` 函数将从数据库中检索上下文，并将其转换为我们用来创建 ``ChatPromptTemplate`` 的聊天消息列表。

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
================================[1m 系统消息 [0m================================

CREATE TABLE demo.user_profiles AS
(
   username VARCHAR (32) NOT NULL,
   name VARCHAR (32) NOT NULL,
   sex VARCHAR (2) NOT NULL,
   address VARCHAR (64) NOT NULL,
   mail VARCHAR (32) NOT NULL,
   birthdate TIMESTAMP NOT NULL
);
COMMENT ON TABLE demo.user_profiles IS '包含用户资料。';

================================[1m 人类消息 [0m=================================

有多少男性用户？

==================================[1m AI 消息 [0m==================================

select count(1) as num_users
    from demo.user_profiles
    where sex = 'M';

================================[1m 人类消息 [0m=================================

[33;1m[1;3m{input}[0m
```

### 创建链

这个链的最后一个元素是 `KineticaSqlOutputParser`，它将执行 SQL 并返回一个数据框。这是可选的，如果我们省略它，则只会返回 SQL。

```python
from langchain_community.chat_models.kinetica import (
    KineticaSqlOutputParser,
    KineticaSqlResponse,
)

chain = prompt_template | kinetica_llm | KineticaSqlOutputParser(kdbc=kinetica_llm.kdbc)
```

### 生成 SQL

我们创建的链将接受一个问题作为输入，并返回一个 ``KineticaSqlResponse``，其中包含生成的 SQL 和数据。问题必须与我们用于创建提示的 LLM 上下文相关。

```python
# 在这里，您必须提出一个与提示模板中提供的 LLM 上下文相关的问题。
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

## 相关

- 聊天模型 [概念指南](/docs/concepts/#chat-models)
- 聊天模型 [使用指南](/docs/how_to/#chat-models)