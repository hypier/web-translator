---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/document_loaders/google_bigtable.ipynb
---

# Google Bigtable

> [Bigtable](https://cloud.google.com/bigtable) 是一个键值和宽列存储，适合快速访问结构化、半结构化或非结构化数据。扩展您的数据库应用程序，构建利用 Bigtable 的 Langchain 集成的 AI 驱动体验。

本笔记本介绍了如何使用 [Bigtable](https://cloud.google.com/bigtable) 通过 `BigtableLoader` 和 `BigtableSaver` [保存、加载和删除 langchain 文档](/docs/how_to#document-loaders)。

在 [GitHub](https://github.com/googleapis/langchain-google-bigtable-python/) 上了解更多关于该包的信息。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googleapis/langchain-google-bigtable-python/blob/main/docs/document_loader.ipynb)

## 开始之前

要运行此笔记本，您需要执行以下操作：

* [创建 Google Cloud 项目](https://developers.google.com/workspace/guides/create-project)
* [启用 Bigtable API](https://console.cloud.google.com/flows/enableapi?apiid=bigtable.googleapis.com)
* [创建 Bigtable 实例](https://cloud.google.com/bigtable/docs/creating-instance)
* [创建 Bigtable 表](https://cloud.google.com/bigtable/docs/managing-tables)
* [创建 Bigtable 访问凭据](https://developers.google.com/workspace/guides/create-credentials)

在确认可以访问此笔记本的运行时环境中的数据库后，请填写以下值并在运行示例脚本之前运行该单元。

```python
# @markdown 请为演示目的指定一个实例和一个表。
INSTANCE_ID = "my_instance"  # @param {type:"string"}
TABLE_ID = "my_table"  # @param {type:"string"}
```

### 🦜🔗 库安装

集成位于其自己的 `langchain-google-bigtable` 包中，因此我们需要安装它。

```python
%pip install -upgrade --quiet langchain-google-bigtable
```

**仅限 Colab**：取消注释以下单元以重启内核，或使用按钮重启内核。对于 Vertex AI Workbench，您可以使用顶部的按钮重启终端。

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
# @markdown 请在下方填写您的 Google Cloud 项目 ID，然后运行该单元格。

PROJECT_ID = "my-project-id"  # @param {type:"string"}

# 设置项目 ID
!gcloud config set project {PROJECT_ID}
```

### 🔐 身份验证

以已登录此笔记本的 IAM 用户身份对 Google Cloud 进行身份验证，以便访问您的 Google Cloud 项目。

- 如果您正在使用 Colab 运行此笔记本，请使用下面的单元并继续。
- 如果您正在使用 Vertex AI Workbench，请查看 [此处](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) 的设置说明。


```python
from google.colab import auth

auth.authenticate_user()
```

## 基本用法

### 使用 saver

使用 `BigtableSaver.add_documents(<documents>)` 保存 langchain 文档。要初始化 `BigtableSaver` 类，您需要提供两样东西：

1. `instance_id` - Bigtable 的实例。
1. `table_id` - 在 Bigtable 中存储 langchain 文档的表名。

```python
from langchain_core.documents import Document
from langchain_google_bigtable import BigtableSaver

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

saver = BigtableSaver(
    instance_id=INSTANCE_ID,
    table_id=TABLE_ID,
)

saver.add_documents(test_docs)
```

### 从 Bigtable 查询文档
有关连接到 Bigtable 表的更多详细信息，请查看 [Python SDK 文档](https://cloud.google.com/python/docs/reference/bigtable/latest/client)。

#### 从表中加载文档

使用 `BigtableLoader.load()` 或 `BigtableLoader.lazy_load()` 加载 langchain 文档。`lazy_load` 返回一个生成器，该生成器仅在迭代期间查询数据库。要初始化 `BigtableLoader` 类，您需要提供：

1. `instance_id` - Bigtable 的实例。
1. `table_id` - 用于存储 langchain 文档的 Bigtable 中的表名。


```python
from langchain_google_bigtable import BigtableLoader

loader = BigtableLoader(
    instance_id=INSTANCE_ID,
    table_id=TABLE_ID,
)

for doc in loader.lazy_load():
    print(doc)
    break
```

### 删除文档

使用 `BigtableSaver.delete(<documents>)` 从 Bigtable 表中删除一系列 langchain 文档。


```python
from langchain_google_bigtable import BigtableSaver

docs = loader.load()
print("Documents before delete: ", docs)

onedoc = test_docs[0]
saver.delete([onedoc])
print("Documents after delete: ", loader.load())
```

## 高级用法

### 限制返回的行数
有两种方法可以限制返回的行数：

1. 使用 [filter](https://cloud.google.com/python/docs/reference/bigtable/latest/row-filters)
2. 使用 [row_set](https://cloud.google.com/python/docs/reference/bigtable/latest/row-set#google.cloud.bigtable.row_set.RowSet)


```python
import google.cloud.bigtable.row_filters as row_filters

filter_loader = BigtableLoader(
    INSTANCE_ID, TABLE_ID, filter=row_filters.ColumnQualifierRegexFilter(b"os_build")
)


from google.cloud.bigtable.row_set import RowSet

row_set = RowSet()
row_set.add_row_range_from_keys(
    start_key="phone#4c410523#20190501", end_key="phone#4c410523#201906201"
)

row_set_loader = BigtableLoader(
    INSTANCE_ID,
    TABLE_ID,
    row_set=row_set,
)
```

### 自定义客户端
默认创建的客户端是默认客户端，仅使用 admin=True 选项。要使用非默认客户端，可以将 [自定义客户端](https://cloud.google.com/python/docs/reference/bigtable/latest/client#class-googlecloudbigtableclientclientprojectnone-credentialsnone-readonlyfalse-adminfalse-clientinfonone-clientoptionsnone-adminclientoptionsnone-channelnone) 传递给构造函数。

```python
from google.cloud import bigtable

custom_client_loader = BigtableLoader(
    INSTANCE_ID,
    TABLE_ID,
    client=bigtable.Client(...),
)
```

### 自定义内容
BigtableLoader 假设存在一个名为 `langchain` 的列族，该列族中有一个名为 `content` 的列，包含以 UTF-8 编码的值。这些默认值可以如下更改：

```python
from langchain_google_bigtable import Encoding

custom_content_loader = BigtableLoader(
    INSTANCE_ID,
    TABLE_ID,
    content_encoding=Encoding.ASCII,
    content_column_family="my_content_family",
    content_column_name="my_content_column_name",
)
```

### 元数据映射
默认情况下，`Document` 对象上的 `metadata` 映射将包含一个键 `rowkey`，其值为行的 rowkey 值。要向该映射添加更多项，请使用 metadata_mapping。

```python
import json

from langchain_google_bigtable import MetadataMapping

metadata_mapping_loader = BigtableLoader(
    INSTANCE_ID,
    TABLE_ID,
    metadata_mappings=[
        MetadataMapping(
            column_family="my_int_family",
            column_name="my_int_column",
            metadata_key="key_in_metadata_map",
            encoding=Encoding.INT_BIG_ENDIAN,
        ),
        MetadataMapping(
            column_family="my_custom_family",
            column_name="my_custom_column",
            metadata_key="custom_key",
            encoding=Encoding.CUSTOM,
            custom_decoding_func=lambda input: json.loads(input.decode()),
            custom_encoding_func=lambda input: str.encode(json.dumps(input)),
        ),
    ],
)
```

### 将元数据作为 JSON

如果 Bigtable 中有一列包含您希望添加到输出文档元数据的 JSON 字符串，可以将以下参数添加到 BigtableLoader。请注意，`metadata_as_json_encoding` 的默认值是 UTF-8。

```python
metadata_as_json_loader = BigtableLoader(
    INSTANCE_ID,
    TABLE_ID,
    metadata_as_json_encoding=Encoding.ASCII,
    metadata_as_json_family="my_metadata_as_json_family",
    metadata_as_json_name="my_metadata_as_json_column_name",
)
```

### 自定义 BigtableSaver

BigtableSaver 也可以像 BigtableLoader 一样进行自定义。

```python
saver = BigtableSaver(
    INSTANCE_ID,
    TABLE_ID,
    client=bigtable.Client(...),
    content_encoding=Encoding.ASCII,
    content_column_family="my_content_family",
    content_column_name="my_content_column_name",
    metadata_mappings=[
        MetadataMapping(
            column_family="my_int_family",
            column_name="my_int_column",
            metadata_key="key_in_metadata_map",
            encoding=Encoding.INT_BIG_ENDIAN,
        ),
        MetadataMapping(
            column_family="my_custom_family",
            column_name="my_custom_column",
            metadata_key="custom_key",
            encoding=Encoding.CUSTOM,
            custom_decoding_func=lambda input: json.loads(input.decode()),
            custom_encoding_func=lambda input: str.encode(json.dumps(input)),
        ),
    ],
    metadata_as_json_encoding=Encoding.ASCII,
    metadata_as_json_family="my_metadata_as_json_family",
    metadata_as_json_name="my_metadata_as_json_column_name",
)
```

## 相关

- 文档加载器 [概念指南](/docs/concepts/#document-loaders)
- 文档加载器 [操作指南](/docs/how_to/#document-loaders)