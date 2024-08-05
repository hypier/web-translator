---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/document_loaders/google_spanner.ipynb
---

# Google Spanner

> [Spanner](https://cloud.google.com/spanner) 是一个高度可扩展的数据库，它将无限的可扩展性与关系语义相结合，例如二级索引、强一致性、模式和 SQL，提供 99.999% 的可用性，提供一个简单的解决方案。

本笔记本介绍了如何使用 [Spanner](https://cloud.google.com/spanner) 通过 `SpannerLoader` 和 `SpannerDocumentSaver` [保存、加载和删除 langchain 文档](/docs/how_to#document-loaders)。

在 [GitHub](https://github.com/googleapis/langchain-google-spanner-python/) 上了解更多关于该包的信息。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googleapis/langchain-google-spanner-python/blob/main/docs/document_loader.ipynb)

## 开始之前

要运行此笔记本，您需要执行以下操作：

* [创建一个 Google Cloud 项目](https://developers.google.com/workspace/guides/create-project)
* [启用 Cloud Spanner API](https://console.cloud.google.com/flows/enableapi?apiid=spanner.googleapis.com)
* [创建一个 Spanner 实例](https://cloud.google.com/spanner/docs/create-manage-instances)
* [创建一个 Spanner 数据库](https://cloud.google.com/spanner/docs/create-manage-databases)
* [创建一个 Spanner 表](https://cloud.google.com/spanner/docs/create-query-database-console#create-schema)

在确认对该笔记本运行时环境中的数据库的访问权限后，填写以下值并在运行示例脚本之前运行该单元格。

```python
# @markdown 请指定一个实例 ID、一个数据库和一个表以供演示使用。
INSTANCE_ID = "test_instance"  # @param {type:"string"}
DATABASE_ID = "test_database"  # @param {type:"string"}
TABLE_NAME = "test_table"  # @param {type:"string"}
```

### 🦜🔗 库安装

集成位于其自己的 `langchain-google-spanner` 包中，因此我们需要安装它。

```python
%pip install -upgrade --quiet langchain-google-spanner langchain
```

**仅限 Colab**：取消注释以下单元以重新启动内核，或使用按钮重新启动内核。对于 Vertex AI Workbench，您可以使用顶部的按钮重新启动终端。

```python
# # Automatically restart kernel after installs so that your environment can access the new packages
# import IPython

# app = IPython.Application.instance()
# app.kernel.do_shutdown(True)
```

### ☁ 设置您的 Google Cloud 项目
设置您的 Google Cloud 项目，以便您可以在此笔记本中利用 Google Cloud 资源。

如果您不知道您的项目 ID，请尝试以下方法：

* 运行 `gcloud config list`。
* 运行 `gcloud projects list`。
* 查看支持页面：[查找项目 ID](https://support.google.com/googleapi/answer/7014113)。

```python
# @markdown 请输入您的 Google Cloud 项目 ID，然后运行该单元格。

PROJECT_ID = "my-project-id"  # @param {type:"string"}

# 设置项目 ID
!gcloud config set project {PROJECT_ID}
```

### 🔐 身份验证

以已登录此笔记本的 IAM 用户身份对 Google Cloud 进行身份验证，以便访问您的 Google Cloud 项目。

- 如果您正在使用 Colab 运行此笔记本，请使用下面的单元格并继续。
- 如果您正在使用 Vertex AI Workbench，请查看 [这里](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) 的设置说明。


```python
from google.colab import auth

auth.authenticate_user()
```

## 基本用法

### 保存文档

使用 `SpannerDocumentSaver.add_documents(<documents>)` 保存 langchain 文档。要初始化 `SpannerDocumentSaver` 类，您需要提供 3 个参数：

1. `instance_id` - 用于加载数据的 Spanner 实例。
1. `database_id` - 用于加载数据的 Spanner 数据库实例。
1. `table_name` - 在 Spanner 数据库中存储 langchain 文档的表名。

```python
from langchain_core.documents import Document
from langchain_google_spanner import SpannerDocumentSaver

test_docs = [
    Document(
        page_content="Apple Granny Smith 150 0.99 1",
        metadata={"fruit_id": 1},
    ),
    Document(
        page_content="Banana Cavendish 200 0.59 0",
        metadata={"fruit_id": 2},
    ),
    Document(
        page_content="Orange Navel 80 1.29 1",
        metadata={"fruit_id": 3},
    ),
]

saver = SpannerDocumentSaver(
    instance_id=INSTANCE_ID,
    database_id=DATABASE_ID,
    table_name=TABLE_NAME,
)
saver.add_documents(test_docs)
```

### 从 Spanner 查询文档

有关连接到 Spanner 表的更多详细信息，请查看 [Python SDK 文档](https://cloud.google.com/python/docs/reference/spanner/latest)。

#### 从表中加载文档

使用 `SpannerLoader.load()` 或 `SpannerLoader.lazy_load()` 加载 langchain 文档。`lazy_load` 返回一个生成器，该生成器在迭代期间仅查询数据库。要初始化 `SpannerLoader` 类，您需要提供：

1. `instance_id` - 要加载数据的 Spanner 实例。
1. `database_id` - 要加载数据的 Spanner 数据库实例。
1. `query` - 数据库方言的查询。

```python
from langchain_google_spanner import SpannerLoader

query = f"SELECT * from {TABLE_NAME}"
loader = SpannerLoader(
    instance_id=INSTANCE_ID,
    database_id=DATABASE_ID,
    query=query,
)

for doc in loader.lazy_load():
    print(doc)
    break
```

### 删除文档

使用 `SpannerDocumentSaver.delete(<documents>)` 从表中删除一系列 langchain 文档。


```python
docs = loader.load()
print("Documents before delete:", docs)

doc = test_docs[0]
saver.delete([doc])
print("Documents after delete:", loader.load())
```

## 高级用法

### 自定义客户端

默认创建的客户端是默认客户端。要显式传入 `credentials` 和 `project`，可以将自定义客户端传递给构造函数。

```python
from google.cloud import spanner
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file("/path/to/key.json")
custom_client = spanner.Client(project="my-project", credentials=creds)
loader = SpannerLoader(
    INSTANCE_ID,
    DATABASE_ID,
    query,
    client=custom_client,
)
```

### 自定义文档页面内容和元数据

加载器将返回一个包含特定数据列页面内容的文档列表。所有其他数据列将被添加到元数据中。每一行变成一个文档。

#### 自定义页面内容格式

SpannerLoader 假设有一个名为 `page_content` 的列。这些默认值可以这样更改：


```python
custom_content_loader = SpannerLoader(
    INSTANCE_ID, DATABASE_ID, query, content_columns=["custom_content"]
)
```

如果指定多个列，页面内容的字符串格式将默认为 `text`（以空格分隔的字符串连接）。用户可以指定其他格式，包括 `text`、`JSON`、`YAML`、`CSV`。

#### 自定义元数据格式

SpannerLoader 假设有一个名为 `langchain_metadata` 的元数据列，用于存储 JSON 数据。元数据列将用作基础字典。默认情况下，所有其他列的数据将被添加，并可能覆盖原始值。这些默认值可以这样更改：


```python
custom_metadata_loader = SpannerLoader(
    INSTANCE_ID, DATABASE_ID, query, metadata_columns=["column1", "column2"]
)
```

#### 自定义 JSON 元数据列名称

默认情况下，加载器使用 `langchain_metadata` 作为基础字典。这可以自定义以选择一个 JSON 列作为文档元数据的基础字典。 


```python
custom_metadata_json_loader = SpannerLoader(
    INSTANCE_ID, DATABASE_ID, query, metadata_json_column="another-json-column"
)
```

### 自定义陈旧性

默认的 [陈旧性](https://cloud.google.com/python/docs/reference/spanner/latest/snapshot-usage#beginning-a-snapshot) 为 15 秒。可以通过指定较弱的边界进行自定义（这可以是以给定时间戳进行的所有读取），或者是过去给定持续时间的读取。

```python
import datetime

timestamp = datetime.datetime.utcnow()
custom_timestamp_loader = SpannerLoader(
    INSTANCE_ID,
    DATABASE_ID,
    query,
    staleness=timestamp,
)
```

```python
duration = 20.0
custom_duration_loader = SpannerLoader(
    INSTANCE_ID,
    DATABASE_ID,
    query,
    staleness=duration,
)
```

### 开启数据增强

默认情况下，加载器不会使用 [数据增强](https://cloud.google.com/spanner/docs/databoost/databoost-overview)，因为这会产生额外的费用，并且需要额外的 IAM 权限。不过，用户可以选择开启它。

```python
custom_databoost_loader = SpannerLoader(
    INSTANCE_ID,
    DATABASE_ID,
    query,
    databoost=True,
)
```

### 自定义客户端

默认创建的客户端是默认客户端。要显式传入 `credentials` 和 `project`，可以将自定义客户端传递给构造函数。

```python
from google.cloud import spanner

custom_client = spanner.Client(project="my-project", credentials=creds)
saver = SpannerDocumentSaver(
    INSTANCE_ID,
    DATABASE_ID,
    TABLE_NAME,
    client=custom_client,
)
```

### SpannerDocumentSaver 的自定义初始化

SpannerDocumentSaver 允许自定义初始化。这使用户可以指定如何将文档保存到表中。

content_column: 这将作为文档页面内容的列名。默认为 `page_content`。

metadata_columns: 如果文档的元数据中存在键，这些元数据将被保存到特定的列中。

metadata_json_column: 这将是特殊 JSON 列的列名。默认为 `langchain_metadata`。


```python
custom_saver = SpannerDocumentSaver(
    INSTANCE_ID,
    DATABASE_ID,
    TABLE_NAME,
    content_column="my-content",
    metadata_columns=["foo"],
    metadata_json_column="my-special-json-column",
)
```

### 初始化 Spanner 的自定义模式

SpannerDocumentSaver 将有一个 `init_document_table` 方法来创建一个新的表以存储具有自定义模式的文档。


```python
from langchain_google_spanner import Column

new_table_name = "my_new_table"

SpannerDocumentSaver.init_document_table(
    INSTANCE_ID,
    DATABASE_ID,
    new_table_name,
    content_column="my-page-content",
    metadata_columns=[
        Column("category", "STRING(36)", True),
        Column("price", "FLOAT64", False),
    ],
)
```

## 相关

- 文档加载器 [概念指南](/docs/concepts/#document-loaders)
- 文档加载器 [操作指南](/docs/how_to/#document-loaders)