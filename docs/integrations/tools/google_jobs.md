---
custom_edit_url: https://github.com/langchain-ai/langchain/edit/master/docs/docs/integrations/tools/google_jobs.ipynb
---

# Google Jobs

本笔记本介绍如何使用 Google Jobs Tool 获取当前的职位发布。

首先，您需要在 https://serpapi.com/users/sign_up 注册一个 `SerpApi key`。

然后，您必须使用以下命令安装 `google-search-results`：
    `pip install google-search-results`

接下来，您需要将环境变量 `SERPAPI_API_KEY` 设置为您的 `SerpApi key`。

如果您还没有一个，可以在 https://serpapi.com/users/sign_up 注册一个免费账户，并在这里获取您的 API 密钥： https://serpapi.com/manage-api-key

如果您使用的是 conda 环境，可以在内核中使用以下命令进行设置：
conda activate [your env name]
conda env confiv vars SERPAPI_API_KEY='[your serp api key]'

## 使用工具


```python
%pip install --upgrade --quiet  google-search-results langchain-community
```
```output
Requirement already satisfied: google-search-results in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (2.4.2)
Requirement already satisfied: requests in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (from google-search-results) (2.31.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (from requests->google-search-results) (3.3.2)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (from requests->google-search-results) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (from requests->google-search-results) (2.1.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/envs/langchain/lib/python3.10/site-packages (from requests->google-search-results) (2023.11.17)
```

```python
import os

from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper

os.environ["SERPAPI_API_KEY"] = "[your serpapi key]"
tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
```


```python
tool.run("Can I get an entry level job posting related to physics")
```



```output
"\n_______________________________________________\n职位名称：应用物理学家（经验丰富或高级）\n公司名称：波音\n地点：加利福尼亚州亨廷顿海滩\n描述：职位描述\n\n在波音，我们创新并合作，使世界变得更美好。从海底到外太空，您可以为一个重视多样性、公平和包容的公司贡献重要的工作。我们致力于为每位团队成员创造一个欢迎、尊重和包容的环境，并提供良好的职业发展机会。与我们一起找到您的未来。\n\n我们是波音研究与技术（BR&T）：波音的全球研究与开发团队，创造并实施创新技术，使不可能变为可能，推动航空航天的未来。我们是工程师和技术人员，熟练的科学家和大胆的创新者；加入我们，将您的热情、决心和技能投入到构建未来的工作中！\n\n加入一个利用新兴技术开发创新产品和服务的成长团队。波音在重新构想商业和政府市场航空航天平台的设计、制造和操作的未来方面处于前沿。\n\n该职位位于加利福尼亚州亨廷顿海滩。\n\n职位职责：\n• 开发和验证各种复杂通信、传感器、电子战及其他电磁系统和组件的要求。\n• 开发和验证电磁要求，以满足电气\\电子系统、机械系统、互连和结构。\n• 开发架构，将复杂系统和组件集成到更高层次的系统和平台中。\n• 执行复杂的权衡研究、建模、仿真和其他分析形式，以预测组件、互连和系统性能，并围绕既定要求优化设计。\n• 定义并进行各种关键测试，以验证设计的性能是否符合要求。管理关键供应商和合作伙伴性能的适当方面，以确保符合要求。\n• 在产品生命周期的各个阶段提供支持，从制造到客户使用，提供指导和支持以解决复杂问题。\n• 通过协调工作说明、预算、进度和其他所需输入的开发，支持项目管理，并进行适当的审查。\n• 生成提案的主要部分，以支持新业务的发展。\n• 在最小指导下工作。\n\n应用物理学家（经验丰富或高级），BR&T/先进计算技术 – 候选人将运用其量子物理知识，构建实验量子传感或量子网络的综合能力套件。成功的候选人将在以下至少一个领域具有深刻的理论和实验室实践理解：\n• 光学钟\n• 光学时间传输\n• 基于光学频率梳的计量\n• 基于量子网络的量子系统纠缠（例如，原子、离子或量子点系统）\n\n成功的候选人将开发\n• 一个充满活力的研究和开发项目，得到内部和外部资金的支持\n• 撰写项目提案\n• 开发未来产品概念\n• 协助将量子技术整合到波音商业和国防业务的未来产品和服务中\n\n该职位允许远程办公。选定的候选人需要在列出的某个地点现场工作。\n\n该职位要求能够获得美国安全许可，而美国政府要求持有美国国籍。入职后需要获得临时和/或最终的美国机密安全许可。\n\n基本资格（所需技能/经验）\n• 物理、化学、电气工程或与量子传感和/或量子信息科学相关的其他领域的博士学位\n• 撰写并发表研究论文和项目（学术或专业）\n• 在以下一个领域的大学学习和实验室实践：光学钟、光学时间传输、原子干涉仪或基于量子网络的量子系统纠缠（例如，原子、离子或量子点系统）\n\n优先资格（期望技能/经验）\n• 9年以上相关工作经验或教育与经验的等效组合\n• 活跃的美国安全许可\n\n典型教育/经验：\n\n经验丰富：通常通过在工程、计算机科学、数学、物理或化学的认证课程中获得的高级技术教育（例如，学士学位）获得教育/经验，通常需要9年或更多相关工作经验或技术教育与经验的等效组合（例如，博士+4年相关工作经验，硕士+7年相关工作经验）。在美国，ABET认证是首选的，尽管不是必需的，认证标准。\n\n高级：通常通过在工程、计算机科学、数学、物理或化学的认证课程中获得的高级技术教育（例如，学士学位）获得教育/经验，通常需要14年或更多相关工作经验或技术教育与经验的等效组合（例如，博士+9年相关工作经验，硕士+12年相关工作经验）。在美国，ABET认证是首选的，尽管不是必需的，认证标准。\n\n搬迁：该职位根据候选人资格提供搬迁。\n\n波音是一个无毒品的工作场所，录用后申请人和员工在符合我们政策中列出的标准时，可能会接受大麻、可卡因、鸦片类药物、安非他命、PCP和酒精的检测。\n\n班次：该职位为第一班。\n\n在波音，我们努力提供一个全面的薪酬福利包，以吸引、吸引和留住顶尖人才。全面薪酬福利包的元素包括具有竞争力的基本工资和可变薪酬机会。\n\n波音公司还为符合条件的员工提供机会，参加各种福利计划，通常包括健康保险、灵活支出账户、健康储蓄账户、退休储蓄计划、人寿和残疾保险计划，以及提供带薪和无薪休假的多个计划。\n\n可供任何给定员工的具体计划和选项可能因地理位置、雇佣日期和集体谈判协议的适用性等资格因素而有所不同。\n\n请注意，下面显示的薪资信息仅为一般指南。薪资基于候选人的经验和资格，以及市场和业务考虑。\n\n经验丰富的薪资范围：$126,000 – $171,000\n\n高级薪资范围：$155,000 - $210,00\n\n出口控制要求：美国政府出口控制状态：该职位必须符合出口控制合规要求。为满足出口控制合规要求，需为符合22 C.F.R. §120.15定义的“美国人”。“美国人”包括美国公民、合法永久居民、难民或庇护者。\n\n出口控制详情：美国职位，要求为美国人\n\n平等机会雇主：\n\n波音是一个平等机会雇主。雇佣决策不考虑种族、肤色、宗教、国籍、性别、性取向、性别认同、年龄、身体或精神残疾、遗传因素、军事/退伍军人身份或其他受法律保护的特征。\n_______________________________________________\n\n"
```

# 与 langchain 一起使用


```python
import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import OpenAI

OpenAI.api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI()
tools = load_tools(["google-jobs"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
agent.run("给我一个与物理相关的入门级职位发布")
```
```output


[1m> 进入新的 AgentExecutor 链...[0m
[32;1m[1;3m 我应该使用工具搜索与物理相关的职位发布
Action: google_jobs
Action Input: entry level physics[0m
Observation: [36;1m[1;3m
_______________________________________________
职位名称：入门级校准技术员（适合新毕业的物理或电气工程专业）
公司名称：Modis Engineering
地点：华盛顿州埃弗雷特   
描述：在华盛顿州埃弗雷特，Akkodis 提供电子校准技术员的合同转聘职位。

这是一个适合喜欢动手工作的入门级物理、BSEET、BSEE、机电一体化或其他专业毕业生的好机会。或者是拥有 1-5 年经验的技术员...

班次：晚班或夜班

薪资：$28 - $32/小时，视经验而定。

如果表现出色，一旦职位转为全职/固定薪资/直接雇佣职位，薪资可能会增加 $2/小时。
• **将提供全面培训***

工作职责包括：

- 校准和测试光纤测试设备。

- 记录校准过程中收集的数据。

- 识别超出公差的情况。

- 与其他技术员、客户服务代表和客户互动。

资格要求：

- 物理或电气工程学士学位 -- 或 -- 电子学（或类似学科）副学士学位 -- 或 -- 电子经验。

- 必须具备良好的书面和口头沟通能力。

- 具备学校实验室工作或其他地方的基本电路测试/故障排除经验。

- 必须具备基本的计算机技能。

- 先前的校准经验优先。

- 有光纤和计量设备经验者优先。

- 该职位不涉及作为维修技术员的故障排除，但在此领域的经验是可接受且有帮助的。

- 该职位要求良好的工作伦理和学习及成功的意愿。

平等机会雇主/退伍军人/残疾人士

福利包括医疗、牙科、视力保险、FSA、HSA、短期和长期残疾保险，以及 401K 计划。还包括全面的带薪休假计划。

免责声明：这些福利不适用于客户招聘的职位和直接雇佣客户的职位。

要阅读我们的候选人隐私信息声明，了解我们如何使用您的信息，请访问 https://www.modis.com/en-us/candidate-privacy
_______________________________________________

[0m
思考：[32;1m[1;3m 我现在知道最终答案
最终答案：与物理相关的入门级职位发布是华盛顿州埃弗雷特的 Modis Engineering 的校准技术员。该职位提供竞争力的薪资 $28 - $32/小时，并将提供全面培训。资格要求包括物理或电气工程学士学位，或电子学或类似学科的副学士学位，福利包括医疗、牙科、视力等。[0m

[1m> 完成链。[0m
```


```output
'与物理相关的入门级职位发布是华盛顿州埃弗雷特的 Modis Engineering 的校准技术员。该职位提供竞争力的薪资 $28 - $32/小时，并将提供全面培训。资格要求包括物理或电气工程学士学位，或电子学或类似学科的副学士学位，福利包括医疗、牙科、视力等。'
```

## 相关

- 工具 [概念指南](/docs/concepts/#tools)
- 工具 [操作指南](/docs/how_to/#tools)