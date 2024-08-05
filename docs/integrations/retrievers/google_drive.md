---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/retrievers/google_drive.ipynb
---

# Google Drive

本笔记本介绍如何从 `Google Drive` 中检索文档。

## 前提条件

1. 创建一个 Google Cloud 项目或使用现有项目
1. 启用 [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com)
1. [为桌面应用授权凭据](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application)
1. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

## 检索 Google 文档

默认情况下，`GoogleDriveRetriever` 期望 `credentials.json` 文件位于 `~/.credentials/credentials.json`，但可以使用 `GOOGLE_ACCOUNT_FILE` 环境变量进行配置。 `token.json` 的位置使用相同的目录（或使用参数 `token_path`）。请注意，第一次使用检索器时将自动创建 `token.json`。

`GoogleDriveRetriever` 可以通过一些请求检索一组选定的文件。

默认情况下，如果使用 `folder_id`，则可以将该文件夹内的所有文件检索到 `Document`。

您可以从 URL 中获取文件夹和文档 ID：

* 文件夹: https://drive.google.com/drive/u/0/folders/1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5 -> 文件夹 ID 为 `"1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5"`
* 文档: https://docs.google.com/document/d/1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw/edit -> 文档 ID 为 `"1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw"`

特殊值 `root` 是您的个人主页。

```python
from langchain_googledrive.retrievers import GoogleDriveRetriever

folder_id = "root"
# folder_id='1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5'

retriever = GoogleDriveRetriever(
    num_results=2,
)
```

默认情况下，所有具有以下 MIME 类型的文件可以转换为 `Document`。

- `text/text`
- `text/plain`
- `text/html`
- `text/csv`
- `text/markdown`
- `image/png`
- `image/jpeg`
- `application/epub+zip`
- `application/pdf`
- `application/rtf`
- `application/vnd.google-apps.document` (GDoc)
- `application/vnd.google-apps.presentation` (GSlide)
- `application/vnd.google-apps.spreadsheet` (GSheet)
- `application/vnd.google.colaboratory` (Notebook colab)
- `application/vnd.openxmlformats-officedocument.presentationml.presentation` (PPTX)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (DOCX)

可以更新或自定义此设置。请参阅 `GoogleDriveRetriever` 的文档。

但是，必须安装相应的包。

```python
%pip install --upgrade --quiet  unstructured
```

```python
retriever.invoke("machine learning")
```

您可以自定义选择文件的标准。提供了一组预定义的过滤器：

| 模板                                     | 描述                                                               |
| ---------------------------------------- | ------------------------------------------------------------------ |
| `gdrive-all-in-folder`                  | 从 `folder_id` 返回所有兼容文件                                     |
| `gdrive-query`                          | 在所有驱动器中搜索 `query`                                        |
| `gdrive-by-name`                        | 按名称 `query` 搜索文件                                           |
| `gdrive-query-in-folder`                | 在 `folder_id` 中搜索 `query`（并在 `_recursive=true` 中的子文件夹中） |
| `gdrive-mime-type`                      | 搜索特定的 `mime_type`                                            |
| `gdrive-mime-type-in-folder`            | 在 `folder_id` 中搜索特定的 `mime_type`                          |
| `gdrive-query-with-mime-type`           | 使用特定的 `mime_type` 搜索 `query`                               |
| `gdrive-query-with-mime-type-and-folder`| 使用特定的 `mime_type` 并在 `folder_id` 中搜索 `query`          |

```python
retriever = GoogleDriveRetriever(
    template="gdrive-query",  # 在所有地方搜索
    num_results=2,  # 但只取 2 个文档
)
for doc in retriever.invoke("machine learning"):
    print("---")
    print(doc.page_content.strip()[:60] + "...")
```

否则，您可以使用专业的 `PromptTemplate` 自定义提示。

```python
from langchain_core.prompts import PromptTemplate

retriever = GoogleDriveRetriever(
    template=PromptTemplate(
        input_variables=["query"],
        # 请参见 https://developers.google.com/drive/api/guides/search-files
        template="(fullText contains '{query}') "
        "and mimeType='application/vnd.google-apps.document' "
        "and modifiedTime > '2000-01-01T00:00:00' "
        "and trashed=false",
    ),
    num_results=2,
    # 请参见 https://developers.google.com/drive/api/v3/reference/files/list
    includeItemsFromAllDrives=False,
    supportsAllDrives=False,
)
for doc in retriever.invoke("machine learning"):
    print(f"{doc.metadata['name']}:")
    print("---")
    print(doc.page_content.strip()[:60] + "...")
```

## 使用 Google Drive 的“描述”元数据

每个 Google Drive 在元数据中都有一个 `description` 字段（请参阅*文件详细信息*）。  
使用 `snippets` 模式返回所选文件的描述。

```python
retriever = GoogleDriveRetriever(
    template="gdrive-mime-type-in-folder",
    folder_id=folder_id,
    mime_type="application/vnd.google-apps.document",  # 仅限 Google 文档
    num_results=2,
    mode="snippets",
    includeItemsFromAllDrives=False,
    supportsAllDrives=False,
)
retriever.invoke("machine learning")
```

## 相关

- Retriever [概念指南](/docs/concepts/#retrievers)
- Retriever [操作指南](/docs/how_to/#retrievers)