# 代码审计报告:vulnerable_agent.py(故意有漏洞的 AI Agent)

> 评测对象:一个 AI Agent 的工具实现(`vulnerable_agent.py`)。
> 方法:静态扫描(`audit_scan.py`)定位入口 + 人工确认数据流与可利用性。
> 结论:发现 **7 类高/中危漏洞**,均可导致代码执行、数据泄露或越权。

## 审计概览

| 编号 | 漏洞 | 位置 | 等级 | OWASP |
|------|------|------|:--:|------|
| V1 | 任意代码执行(eval LLM 输出) | `run_code_tool` | 严重 | LLM02 不安全输出处理 |
| V2 | 命令注入(shell=True 拼接) | `shell_tool` | 严重 | A03 / LLM06 |
| V3 | SSRF(无白名单的 URL 请求) | `fetch_url_tool` | 高 | A10 / LLM06 |
| V4 | 路径穿越(拼接用户路径) | `read_file_tool` | 高 | A01 |
| V5 | SQL 注入(f-string 拼 SQL) | `query_user_tool` | 高 | A03 |
| V6 | 不安全反序列化(pickle) | `load_state_tool` | 严重 | A08 |
| V7 | 过度授权(高危动作无校验) | `issue_refund_tool` | 高 | LLM06 |
| V0 | 硬编码机密 | 模块顶部 | 高 | A05 |

## 逐项分析

### V1 · 任意代码执行(严重)
- **位置**:`run_code_tool`:`return eval(llm_output)`
- **数据流**:大模型/用户输出 → 直接进入 `eval` → 作为 Python 代码执行。
- **风险**:攻击者通过提示注入控制 LLM 输出,即可执行任意代码(读文件、反弹shell等)。
- **PoC 思路**:让 LLM 输出 `__import__('os').system('id')` 类字符串。
- **修复**:**禁止 eval/exec 处理模型或用户内容**;需要结构化结果用 `ast.literal_eval` 或 JSON 解析;计算类用受限沙箱。

### V2 · 命令注入(严重)
- **位置**:`shell_tool`:`subprocess.run(f"cat {filename}", shell=True)`
- **数据流**:用户 filename → 拼进命令字符串 → 交给 shell 解析。
- **风险**:`filename = "x; rm -rf /"` 可执行额外命令。
- **修复**:`shell=False` + 参数列表;文件名做白名单/规范化;能不调 shell 就用语言 API。

### V3 · SSRF(高)
- **位置**:`fetch_url_tool`:`requests.get(url)`,url 来自用户/LLM。
- **风险**:访问内网服务、云元数据(169.254.169.254)、`file://`、`localhost` 管理端口。
- **PoC 思路**:`url = "http://169.254.169.254/latest/meta-data/"`。
- **修复**:URL 白名单(协议/域名);解析后**拒绝私有/保留 IP**;禁用重定向跟随到内网;出网代理隔离。

### V4 · 路径穿越(高)
- **位置**:`read_file_tool`:`open(os.path.join("data", path))`,path 可含 `../`。
- **风险**:`path = "../../etc/passwd"` 读取越界文件。
- **修复**:`realpath` 规范化后校验仍在 `data/` 根目录内;或用 ID 映射,不暴露真实路径。

### V5 · SQL 注入(高)
- **位置**:`query_user_tool`:`execute(f"... id = {user_id}")`。
- **风险**:`user_id = "1 OR 1=1"` 拖库;`union select` 读其他表。
- **修复**:参数化查询 `execute("... id = ?", (user_id,))`;ORM;最小权限数据库账号。

### V6 · 不安全反序列化(严重)
- **位置**:`load_state_tool`:`pickle.loads(blob)`,blob 不可信。
- **风险**:构造恶意 pickle,反序列化时通过 `__reduce__` 执行任意代码(RCE)。
- **修复**:**绝不 pickle 反序列化不可信数据**;改用 JSON;必须用 pickle 时加签名校验来源。

### V7 · 过度授权(高)
- **位置**:`issue_refund_tool`:无金额上限、无权限/人工校验。
- **风险**:被劫持的 Agent 直接发起越权大额退款。
- **修复**:工具执行前接入权限审计(见 `../tool-permission-audit`),金额上限 + 人工确认 + 审计日志。

### V0 · 硬编码机密(高)
- **位置**:`SYSTEM_PROMPT` 含管理员密钥、`API_KEY` 硬编码。
- **风险**:源码泄露即机密泄露;系统提示词含机密还可能被提示注入套出。
- **修复**:机密走 `.env`/密钥管理;系统提示词不放可被复述的机密。

## 整改优先级
1. 立即:V1 eval、V6 pickle、V2 命令注入(可直接 RCE)。
2. 高:V3 SSRF、V4 路径穿越、V5 SQL 注入、V7 过度授权、V0 硬编码机密。
3. 复测:整改后重跑 `audit_scan.py`,并对 Agent 接入 `llm-security-gateway` + `tool-permission-audit`。

## 审计方法说明
静态扫描(audit_scan.py)用于**快速定位审计入口**;真实漏洞需人工确认**数据流是否可达、输入是否可控、是否有可利用路径**。本报告即"扫描定位 → 人工确认 → 评级 → 修复建议"的标准代码审计闭环。
