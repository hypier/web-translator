---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/memory/google_firestore_datastore.ipynb
---

# Google Firestore (Datastore 模式)

> [Google Cloud Firestore in Datastore](https://cloud.google.com/datastore) 是一个无服务器的文档导向数据库，可以根据需求进行扩展。扩展您的数据库应用程序，构建利用 `Datastore` 的 Langchain 集成的 AI 驱动体验。

本笔记本介绍了如何使用 [Google Cloud Firestore in Datastore](https://cloud.google.com/datastore) 存储聊天消息历史记录，使用 `DatastoreChatMessageHistory` 类。

在 [GitHub](https://github.com/googleapis/langchain-google-datastore-python/) 上了解有关该软件包的更多信息。

[![在 Colab 中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googleapis/langchain-google-datastore-python/blob/main/docs/chat_message_history.ipynb)

## 开始之前

要运行此笔记本，您需要执行以下操作：

* [创建一个 Google Cloud 项目](https://developers.google.com/workspace/guides/create-project)
* [启用 Datastore API](https://console.cloud.google.com/flows/enableapi?apiid=datastore.googleapis.com)
* [创建一个 Datastore 数据库](https://cloud.google.com/datastore/docs/manage-databases)

在确认对该笔记本运行时环境中数据库的访问权限后，请填写以下值并在运行示例脚本之前运行该单元。

### 🦜🔗 库安装

集成存在于其自己的 `langchain-google-datastore` 包中，因此我们需要安装它。

```python
%pip install -upgrade --quiet langchain-google-datastore
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
# @markdown 请在下面填写您的 Google Cloud 项目 ID，然后运行该单元格。

PROJECT_ID = "my-project-id"  # @param {type:"string"}

# 设置项目 ID
!gcloud config set project {PROJECT_ID}
```

### 🔐 身份验证

以登录此笔记本的 IAM 用户身份对 Google Cloud 进行身份验证，以访问您的 Google Cloud 项目。

- 如果您使用 Colab 运行此笔记本，请使用下面的单元格并继续。
- 如果您使用 Vertex AI Workbench，请查看 [此处](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) 的设置说明。


```python
from google.colab import auth

auth.authenticate_user()
```

### API 启用
`langchain-google-datastore` 包要求您在 Google Cloud 项目中 [启用 Datastore API](https://console.cloud.google.com/flows/enableapi?apiid=datastore.googleapis.com)。

```python
# enable Datastore API
!gcloud services enable datastore.googleapis.com
```

## 基本用法

### DatastoreChatMessageHistory

要初始化 `DatastoreChatMessageHistory` 类，您只需提供 3 个参数：

1. `session_id` - 一个唯一标识符字符串，用于指定会话的 ID。
1. `kind` - 要写入的 Datastore 种类名称。这个值是可选的，默认情况下将使用 `ChatHistory` 作为种类。
1. `collection` - 指向 Datastore 集合的单个 `/` 分隔路径。


```python
from langchain_google_datastore import DatastoreChatMessageHistory

chat_history = DatastoreChatMessageHistory(
    session_id="user-session-id", collection="HistoryMessages"
)

chat_history.add_user_message("Hi!")
chat_history.add_ai_message("How can I help you?")
```


```python
chat_history.messages
```

#### 清理
当特定会话的历史记录过时并且可以从数据库和内存中删除时，可以通过以下方式进行。

**注意：** 一旦删除，数据将不再存储在 Datastore 中，并且将永久丢失。


```python
chat_history.clear()
```

### 自定义客户端

客户端默认使用可用的环境变量创建。可以将[自定义客户端](https://cloud.google.com/python/docs/reference/datastore/latest/client)传递给构造函数。

```python
from google.auth import compute_engine
from google.cloud import datastore

client = datastore.Client(
    project="project-custom",
    database="non-default-database",
    credentials=compute_engine.Credentials(),
)

history = DatastoreChatMessageHistory(
    session_id="session-id", collection="History", client=client
)

history.add_user_message("New message")

history.messages

history.clear()
```