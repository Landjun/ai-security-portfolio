# 01 · 传统安全 (Traditional Security)

Web 与系统层经典漏洞的学习沉淀。每个漏洞按「原理 → 复现 → 防护 → 修复 → 检测 → 面试表达」六步走,全部本地靶场、可一键运行。

## 已完成案例(可运行)

| 案例 | 漏洞 | 看点 |
|------|------|------|
| [SQL 注入](sql-injection/) | OWASP A03 | `admin' --` 绕过登录 → 参数化查询免疫 |
| [跨站脚本 XSS](xss/) | OWASP A03 | `<script>` 注入 → 输出转义 |
| [命令注入](command-injection/) | OWASP A03 | `&&` 追加命令 → 参数列表 + shell=False |
| [路径穿越](path-traversal/) | OWASP A01 | `../` 读越界机密 → 规范化 + 边界校验 |

## 运行

每个目录下:
```powershell
cd 01-traditional-security\<案例名>
python demo.py
```

## 约定与安全边界

- 全部使用**本地靶场**(内存 sqlite3 / 临时目录 / 无害载荷),**不针对任何真实目标**。
- 每个案例一个子目录:`demo.py`(不安全 vs 安全对比)+ `README.md`(六步法)。
