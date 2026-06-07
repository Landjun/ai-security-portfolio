# GitHub 作品集"面试就绪"核对清单

> 投递前/面试前打开仓库逐项核对,确保招聘方第一眼看到的是"专业、可运行、可信"的样子。
> 🟢=我(AI)已处理 · 🔵=需你在浏览器/本机人工确认 · ⚪=可选加分项

## 一、首页观感(招聘方第一屏)
- 🟢 顶部徽章:CI / Python / 45+ 项目 / OWASP 全覆盖 / ATLAS / 技术栈
- 🔵 **CI 徽章是否为绿色 passing**(打开仓库首页看 badge;若红,点进 Actions 看失败日志)
- 🔵 **4 张 Mermaid 图是否正常渲染**(三层能力地图 / 码小安管线 / 安全网关 / 区块链审计闭环)——
      GitHub 偶发 Mermaid 渲染失败会显示报错框,刷新或微调语法即可
- 🟢 量化战绩表(绕过率 53%→0%、AUC 0.93、保真度 95% 等)
- 🟢 全部案例折叠收纳(首页清爽)

## 二、内容准确性
- 🟢 模块数字与真实一致(01:8 / 02:9 / 03:11 / 06:6 / 07:7 / 08:11 / 40 单测)
- 🔵 通读一遍 README,确认没有过时表述或错别字
- 🔵 关键链接可点击(随机点 5~6 个子项目链接确认不 404)

## 三、安全与合规(面试官会扫一眼的"专业度")
- 🟢 `.env` / 密钥已 gitignore;`.env.example` 仅占位
- 🔵 **确认仓库历史里从未提交过真实 API Key**(可在 GitHub 仓库搜 `sk-`、`DEEPSEEK_API_KEY=` 实值)
- 🟢 所有攻防内容标注"仅本地/授权环境、学习与防御研究"
- 🟢 区块链全程"纯静态、不部署不攻击"边界声明

## 四、可运行性(面试官可能 clone 跑)
- 🔵 找一台干净环境 `git clone` 后跑通无 Key 的 demo:
      `python 02-ai-security/prompt-injection/demo.py`
- 🔵 跑全量单测:`python -m unittest discover -s tests`(应 40 passed)
- 🔵 跑区块链扫描器:`python 08-blockchain-security/audit_scanner.py --selftest`(10/10)

## 五、加分项(可选)
- ⚪ **录制码小安演示 gif** 放首页(见 `06-ai-development/ai-coding-helper/docs/RECORD-DEMO.md`)——最直观
- ⚪ 仓库 About/Topics 填关键词(ai-security, llm-security, prompt-injection, agent, blockchain-security)
- ⚪ 置顶仓库(GitHub Profile → Pin)
- ⚪ 发布 1~2 篇配套文章(`articles/` 已有草稿)形成可搜索影响力
- ⚪ 加 LICENSE(如 MIT)与简短 CONTRIBUTING(显得是认真维护的项目)

## 六、投递动作
- 🔵 简历里 GitHub 链接做成**可点击超链接**
- 🔵 按岗位选简历档位:[resume-project-section.md](resume-project-section.md)(精简/标准/完整三档)
- 🔵 自我介绍/打招呼话术:[hr-outreach.md](hr-outreach.md)
- 🔵 面试前挑 3 个能讲深的项目过一遍 STAR:[project-map.md](project-map.md)

> 一句话:**🟢 的我已尽量做完,🔵 的需要你花 15 分钟在浏览器/本机走一遍。** 这是从"代码在那"到"面试加分"的最后一公里。
