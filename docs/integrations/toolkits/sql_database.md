---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/toolkits/sql_database.ipynb
sidebar_label: SQLDatabaseToolkit
---

# SQLDatabaseToolkit

这将帮助您开始使用 SQL 数据库 [工具包](/docs/concepts/#toolkits)。有关所有 `SQLDatabaseToolkit` 功能和配置的详细文档，请访问 [API 参考](https://api.python.langchain.com/en/latest/agent_toolkits/langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit.html)。

`SQLDatabaseToolkit` 中的工具旨在与 `SQL` 数据库进行交互。

一个常见的应用是使代理能够使用关系数据库中的数据回答问题，可能以迭代的方式进行（例如，从错误中恢复）。

**⚠️ 安全提示 ⚠️**

构建 SQL 数据库的问答系统需要执行模型生成的 SQL 查询。这存在固有的风险。确保您的数据库连接权限始终针对您的链/代理的需求尽可能狭窄。这将缓解但不能消除构建模型驱动系统的风险。有关一般安全最佳实践的更多信息，[请参见此处](/docs/security).

## 设置

如果您想从单个工具的运行中获取自动化跟踪，您还可以通过取消注释以下内容来设置您的 [LangSmith](https://docs.smith.langchain.com/) API 密钥：

```python
# os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
# os.environ["LANGSMITH_TRACING"] = "true"
```

### 安装

该工具包位于 `langchain-community` 包中：

```python
%pip install --upgrade --quiet  langchain-community
```

出于演示目的，我们将访问 LangChain [Hub](https://smith.langchain.com/hub) 中的一个提示。我们还需要 `langgraph` 来演示如何使用该工具包与代理。这并不是使用该工具包的必要条件。

```python
%pip install --upgrade --quiet langchainhub langgraph
```

## 实例化

`SQLDatabaseToolkit` 工具包需要：

- 一个 [SQLDatabase](https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.sql_database.SQLDatabase.html) 对象；
- 一个 LLM 或聊天模型（用于实例化 [QuerySQLCheckerTool](https://api.python.langchain.com/en/latest/tools/langchain_community.tools.sql_database.tool.QuerySQLCheckerTool.html) 工具）。

下面，我们将使用这些对象实例化工具包。首先创建一个数据库对象。

本指南使用基于 [这些说明](https://database.guide/2-sample-databases-sqlite/) 的示例 `Chinook` 数据库。

接下来，我们将使用 `requests` 库拉取 `.sql` 文件并创建一个内存中的 SQLite 数据库。请注意，这种方法轻量，但是短暂的且不线程安全。如果您愿意，可以按照说明将文件保存为 `Chinook.db` 并通过 `db = SQLDatabase.from_uri("sqlite:///Chinook.db")` 实例化数据库。


```python
import sqlite3

import requests
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


engine = get_engine_for_chinook_db()

db = SQLDatabase(engine)
```

我们还需要一个 LLM 或聊天模型：

import ChatModelTabs from "@theme/ChatModelTabs";

<ChatModelTabs customVarName="llm" />

现在我们可以实例化工具包：


```python
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
```

## 工具

查看可用工具：

```python
toolkit.get_tools()
```

API 参考：

- [QuerySQLDataBaseTool](https://api.python.langchain.com/en/latest/tools/langchain_community.tools.sql_database.tool.QuerySQLDataBaseTool.html)
- [InfoSQLDatabaseTool](https://api.python.langchain.com/en/latest/tools/langchain_community.tools.sql_database.tool.InfoSQLDatabaseTool.html)
- [ListSQLDatabaseTool](https://api.python.langchain.com/en/latest/tools/langchain_community.tools.sql_database.tool.ListSQLDatabaseTool.html)
- [QuerySQLCheckerTool](https://api.python.langchain.com/en/latest/tools/langchain_community.tools.sql_database.tool.QuerySQLCheckerTool.html)

## 在代理中使用

根据 [SQL Q&A Tutorial](/docs/tutorials/sql_qa/#agents)，下面我们为一个简单的问题回答代理提供工具。首先，我们提取一个相关的提示并用所需参数填充它：

```python
from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
print(prompt_template.input_variables)
```
```output
['dialect', 'top_k']
```

```python
system_message = prompt_template.format(dialect="SQLite", top_k=5)
```

然后我们实例化代理：

```python
from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message
)
```

并向它发出查询：

```python
example_query = "Which country's customers spent the most?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
```
```output
================================[1m Human Message [0m=================================

Which country's customers spent the most?
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_list_tables (call_eiheSxiL0s90KE50XyBnBtJY)
 Call ID: call_eiheSxiL0s90KE50XyBnBtJY
  Args:
=================================[1m Tool Message [0m=================================
Name: sql_db_list_tables

Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_schema (call_YKwGWt4UUVmxxY7vjjBDzFLJ)
 Call ID: call_YKwGWt4UUVmxxY7vjjBDzFLJ
  Args:
    table_names: Customer, Invoice, InvoiceLine
=================================[1m Tool Message [0m=================================
Name: sql_db_schema


CREATE TABLE "Customer" (
	"CustomerId" INTEGER NOT NULL, 
	"FirstName" NVARCHAR(40) NOT NULL, 
	"LastName" NVARCHAR(20) NOT NULL, 
	"Company" NVARCHAR(80), 
	"Address" NVARCHAR(70), 
	"City" NVARCHAR(40), 
	"State" NVARCHAR(40), 
	"Country" NVARCHAR(40), 
	"PostalCode" NVARCHAR(10), 
	"Phone" NVARCHAR(24), 
	"Fax" NVARCHAR(24), 
	"Email" NVARCHAR(60) NOT NULL, 
	"SupportRepId" INTEGER, 
	PRIMARY KEY ("CustomerId"), 
	FOREIGN KEY("SupportRepId") REFERENCES "Employee" ("EmployeeId")
)

/*
3 rows from Customer table:
CustomerId	FirstName	LastName	Company	Address	City	State	Country	PostalCode	Phone	Fax	Email	SupportRepId
1	Luís	Gonçalves	Embraer - Empresa Brasileira de Aeronáutica S.A.	Av. Brigadeiro Faria Lima, 2170	São José dos Campos	SP	Brazil	12227-000	+55 (12) 3923-5555	+55 (12) 3923-5566	luisg@embraer.com.br	3
2	Leonie	Köhler	None	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	+49 0711 2842222	None	leonekohler@surfeu.de	5
3	François	Tremblay	None	1498 rue Bélanger	Montréal	QC	Canada	H2G 1A7	+1 (514) 721-4711	None	ftremblay@gmail.com	3
*/


CREATE TABLE "Invoice" (
	"InvoiceId" INTEGER NOT NULL, 
	"CustomerId" INTEGER NOT NULL, 
	"InvoiceDate" DATETIME NOT NULL, 
	"BillingAddress" NVARCHAR(70), 
	"BillingCity" NVARCHAR(40), 
	"BillingState" NVARCHAR(40), 
	"BillingCountry" NVARCHAR(40), 
	"BillingPostalCode" NVARCHAR(10), 
	"Total" NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY ("InvoiceId"), 
	FOREIGN KEY("CustomerId") REFERENCES "Customer" ("CustomerId")
)

/*
3 rows from Invoice table:
InvoiceId	CustomerId	InvoiceDate	BillingAddress	BillingCity	BillingState	BillingCountry	BillingPostalCode	Total
1	2	2021-01-01 00:00:00	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	1.98
2	4	2021-01-02 00:00:00	Ullevålsveien 14	Oslo	None	Norway	0171	3.96
3	8	2021-01-03 00:00:00	Grétrystraat 63	Brussels	None	Belgium	1000	5.94
*/


CREATE TABLE "InvoiceLine" (
	"InvoiceLineId" INTEGER NOT NULL, 
	"InvoiceId" INTEGER NOT NULL, 
	"TrackId" INTEGER NOT NULL, 
	"UnitPrice" NUMERIC(10, 2) NOT NULL, 
	"Quantity" INTEGER NOT NULL, 
	PRIMARY KEY ("InvoiceLineId"), 
	FOREIGN KEY("TrackId") REFERENCES "Track" ("TrackId"), 
	FOREIGN KEY("InvoiceId") REFERENCES "Invoice" ("InvoiceId")
)

/*
3 rows from InvoiceLine table:
InvoiceLineId	InvoiceId	TrackId	UnitPrice	Quantity
1	1	2	0.99	1
2	1	4	0.99	1
3	2	6	0.99	1
*/
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_query (call_7WBDcMxl1h7MnI05njx1q8V9)
 Call ID: call_7WBDcMxl1h7MnI05njx1q8V9
  Args:
    query: SELECT c.Country, SUM(i.Total) AS TotalSpent FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.Country ORDER BY TotalSpent DESC LIMIT 1
=================================[1m Tool Message [0m=================================
Name: sql_db_query

[('USA', 523.0600000000003)]
==================================[1m Ai Message [0m==================================

来自美国的客户消费最多，总金额为 $523.06。
```
我们还可以观察到代理从错误中恢复：

```python
example_query = "Who are the top 3 best selling artists?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
```
```output
================================[1m Human Message [0m=================================

Who are the top 3 best selling artists?
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_query (call_9F6Bp2vwsDkeLW6FsJFqLiet)
 Call ID: call_9F6Bp2vwsDkeLW6FsJFqLiet
  Args:
    query: SELECT artist_name, SUM(quantity) AS total_sold FROM sales GROUP BY artist_name ORDER BY total_sold DESC LIMIT 3
=================================[1m Tool Message [0m=================================
Name: sql_db_query

Error: (sqlite3.OperationalError) no such table: sales
[SQL: SELECT artist_name, SUM(quantity) AS total_sold FROM sales GROUP BY artist_name ORDER BY total_sold DESC LIMIT 3]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_list_tables (call_Gx5adzWnrBDIIxzUDzsn83zO)
 Call ID: call_Gx5adzWnrBDIIxzUDzsn83zO
  Args:
=================================[1m Tool Message [0m=================================
Name: sql_db_list_tables

Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_schema (call_ftywrZgEgGWLrnk9dYC0xtZv)
 Call ID: call_ftywrZgEgGWLrnk9dYC0xtZv
  Args:
    table_names: Artist, Album, InvoiceLine
=================================[1m Tool Message [0m=================================
Name: sql_db_schema


CREATE TABLE "Album" (
	"AlbumId" INTEGER NOT NULL, 
	"Title" NVARCHAR(160) NOT NULL, 
	"ArtistId" INTEGER NOT NULL, 
	PRIMARY KEY ("AlbumId"), 
	FOREIGN KEY("ArtistId") REFERENCES "Artist" ("ArtistId")
)

/*
3 rows from Album table:
AlbumId	Title	ArtistId
1	For Those About To Rock We Salute You	1
2	Balls to the Wall	2
3	Restless and Wild	2
*/


CREATE TABLE "Artist" (
	"ArtistId" INTEGER NOT NULL, 
	"Name" NVARCHAR(120), 
	PRIMARY KEY ("ArtistId")
)

/*
3 rows from Artist table:
ArtistId	Name
1	AC/DC
2	Accept
3	Aerosmith
*/


CREATE TABLE "InvoiceLine" (
	"InvoiceLineId" INTEGER NOT NULL, 
	"InvoiceId" INTEGER NOT NULL, 
	"TrackId" INTEGER NOT NULL, 
	"UnitPrice" NUMERIC(10, 2) NOT NULL, 
	"Quantity" INTEGER NOT NULL, 
	PRIMARY KEY ("InvoiceLineId"), 
	FOREIGN KEY("TrackId") REFERENCES "Track" ("TrackId"), 
	FOREIGN KEY("InvoiceId") REFERENCES "Invoice" ("InvoiceId")
)

/*
3 rows from InvoiceLine table:
InvoiceLineId	InvoiceId	TrackId	UnitPrice	Quantity
1	1	2	0.99	1
2	1	4	0.99	1
3	2	6	0.99	1
*/
==================================[1m Ai Message [0m==================================
Tool Calls:
  sql_db_query (call_i6n3lmS7E2ZivN758VOayTiy)
 Call ID: call_i6n3lmS7E2ZivN758VOayTiy
  Args:
    query: SELECT Artist.Name AS artist_name, SUM(InvoiceLine.Quantity) AS total_sold FROM Artist JOIN Album ON Artist.ArtistId = Album.ArtistId JOIN Track ON Album.AlbumId = Track.AlbumId JOIN InvoiceLine ON Track.TrackId = InvoiceLine.TrackId GROUP BY Artist.Name ORDER BY total_sold DESC LIMIT 3
=================================[1m Tool Message [0m=================================
Name: sql_db_query

[('Iron Maiden', 140), ('U2', 107), ('Metallica', 91)]
==================================[1m Ai Message [0m==================================

排名前三的畅销艺术家是：
1. Iron Maiden - 售出 140 件
2. U2 - 售出 107 件
3. Metallica - 售出 91 件
```

## 特定功能

`SQLDatabaseToolkit` 实现了一个 [.get_context](https://api.python.langchain.com/en/latest/agent_toolkits/langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit.html#langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit.get_context) 方法，方便在提示或其他上下文中使用。

**⚠️ 免责声明 ⚠️** : 代理可能会生成插入/更新/删除查询。当这不是预期时，请使用自定义提示或创建没有写权限的 SQL 用户。

最终用户可能会通过询问简单的问题，例如“运行可能的最大查询”，来超载您的 SQL 数据库。生成的查询可能如下所示：

```sql
SELECT * FROM "public"."users"
    JOIN "public"."user_permissions" ON "public"."users".id = "public"."user_permissions".user_id
    JOIN "public"."projects" ON "public"."users".id = "public"."projects".user_id
    JOIN "public"."events" ON "public"."projects".id = "public"."events".project_id;
```

对于一个事务性 SQL 数据库，如果上述表中的某一个包含数百万行，查询可能会对使用同一数据库的其他应用程序造成麻烦。

大多数面向数据仓库的数据库支持用户级配额，以限制资源使用。

## API 参考

有关所有 SQLDatabaseToolkit 功能和配置的详细文档，请访问 [API 参考](https://api.python.langchain.com/en/latest/agent_toolkits/langchain_community.agent_toolkits.sql.toolkit.SQLDatabaseToolkit.html)。