---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/document_loaders/microsoft_onenote.ipynb
---

# Microsoft OneNote

本笔记本涵盖了如何从 `OneNote` 加载文档。

## 前提条件
1. 按照 [Microsoft 身份平台](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) 的说明注册一个应用程序。
2. 注册完成后，Azure 门户会显示应用注册的概述面板。您会看到应用程序（客户端）ID。此值也称为 `client ID`，它唯一标识您在 Microsoft 身份平台上的应用程序。
3. 在您将要遵循的 **第 1 项** 步骤中，可以将重定向 URI 设置为 `http://localhost:8000/callback`
4. 在您将要遵循的 **第 1 项** 步骤中，在应用程序机密部分生成一个新密码（`client_secret`）。
5. 按照此 [文档](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-expose-web-apis#add-a-scope) 的说明将以下 `SCOPES`（`Notes.Read`）添加到您的应用程序。
6. 您需要使用命令 `pip install msal` 和 `pip install beautifulsoup4` 安装 msal 和 bs4 包。
7. 在步骤结束时，您必须拥有以下值：
- `CLIENT_ID`
- `CLIENT_SECRET`

## 🧑 从 OneNote 导入文档的说明

### 🔑 认证

默认情况下，`OneNoteLoader` 期望 `CLIENT_ID` 和 `CLIENT_SECRET` 的值分别存储为名为 `MS_GRAPH_CLIENT_ID` 和 `MS_GRAPH_CLIENT_SECRET` 的环境变量。您可以通过在应用程序根目录下的 `.env` 文件传递这些环境变量，或在脚本中使用以下命令。

```python
os.environ['MS_GRAPH_CLIENT_ID'] = "YOUR CLIENT ID"
os.environ['MS_GRAPH_CLIENT_SECRET'] = "YOUR CLIENT SECRET"
```

该加载器使用一种称为 [*代表用户进行身份验证*](https://learn.microsoft.com/en-us/graph/auth-v2-user?context=graph%2Fapi%2F1.0&view=graph-rest-1.0) 的身份验证方式。这是一种需要用户同意的两步身份验证。当您实例化加载器时，它将打印一个 URL，用户必须访问该 URL 以对应用程序所需权限给予同意。然后，用户必须访问此 URL 并对应用程序给予同意。接着，用户必须复制结果页面的 URL 并将其粘贴回控制台。如果登录尝试成功，该方法将返回 True。

```python
from langchain_community.document_loaders.onenote import OneNoteLoader

loader = OneNoteLoader(notebook_name="NOTEBOOK NAME", section_name="SECTION NAME", page_title="PAGE TITLE")
```

一旦完成身份验证，加载器将在 `~/.credentials/` 文件夹中存储一个令牌 (`onenote_graph_token.txt`)。此令牌可用于后续的身份验证，而无需重复之前的复制/粘贴步骤。要使用此令牌进行身份验证，您需要在加载器的实例化过程中将 `auth_with_token` 参数更改为 True。

```python
from langchain_community.document_loaders.onenote import OneNoteLoader

loader = OneNoteLoader(notebook_name="NOTEBOOK NAME", section_name="SECTION NAME", page_title="PAGE TITLE", auth_with_token=True)
```

另外，您也可以直接将令牌传递给加载器。这在您希望使用由其他应用程序生成的令牌进行身份验证时非常有用。例如，您可以使用 [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) 生成一个令牌，然后将其传递给加载器。

```python
from langchain_community.document_loaders.onenote import OneNoteLoader

loader = OneNoteLoader(notebook_name="NOTEBOOK NAME", section_name="SECTION NAME", page_title="PAGE TITLE", access_token="TOKEN")
```

### 🗂️ 文档加载器

#### 📑 从 OneNote 笔记本加载页面

`OneNoteLoader` 可以从存储在 OneDrive 中的 OneNote 笔记本加载页面。您可以指定 `notebook_name`、`section_name`、`page_title` 的任意组合，以分别过滤特定笔记本、特定部分或特定标题下的页面。例如，您想加载存储在名为 `Recipes` 的部分下的所有页面，这些页面位于您的任何 OneDrive 笔记本中。

```python
from langchain_community.document_loaders.onenote import OneNoteLoader

loader = OneNoteLoader(section_name="Recipes", auth_with_token=True)
documents = loader.load()
```

#### 📑 从页面 ID 列表加载页面

另一种可能性是提供要加载的每个页面的 `object_ids` 列表。为此，您需要查询 [Microsoft Graph API](https://developer.microsoft.com/en-us/graph/graph-explorer) 以找到您感兴趣的所有文档 ID。此 [链接](https://learn.microsoft.com/en-us/graph/onenote-get-content#page-collection) 提供了一系列端点，可帮助您检索文档 ID。

例如，要检索存储在您的笔记本中的所有页面的信息，您需要向以下地址发送请求：`https://graph.microsoft.com/v1.0/me/onenote/pages`。一旦您获得了感兴趣的 ID 列表，您就可以使用以下参数实例化加载器。

```python
from langchain_community.document_loaders.onenote import OneNoteLoader

loader = OneNoteLoader(object_ids=["ID_1", "ID_2"], auth_with_token=True)
documents = loader.load()
```

## 相关

- 文档加载器 [概念指南](/docs/concepts/#document-loaders)
- 文档加载器 [操作指南](/docs/how_to/#document-loaders)