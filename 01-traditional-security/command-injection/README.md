# 案例:命令注入 (Command Injection)

> `01 传统安全` 案例。演示拼接 shell 命令的危险与安全调用方式。对应 OWASP Top 10 A03:Injection。
> ⚠️ 本演示使用**无害载荷**(追加一个 echo),不执行任何危险命令。

## 1. 原理

应用把用户输入拼进 shell 命令并交给 shell 执行时,攻击者可用 `;`、`&&`、`|` 等
追加额外命令。例如文件名输入 `report.txt && rm -rf /`,被拼接后 shell 会先处理文件、
再执行删除。本演示用无害的 `&& echo ...` 体现"多执行了一条命令"。

## 2. 复现环境

```
command-injection/
├── demo.py    # 不安全(拼接+shell=True) vs 安全(参数列表+shell=False)
└── README.md
```

## 3. 防护方案

1. **不经过 shell**(首选):用参数列表调用(`subprocess.run([...], shell=False)`),输入只当参数。
2. **避免调用外部命令**:能用语言内置 API(如文件操作)就不要 shell 出去。
3. **严格白名单**:确需拼接时,对参数做白名单/转义(如 `shlex.quote`)。
4. **最小权限**:运行进程用低权限账号,降低被注入后的损失。

## 4. 修复建议

- 把 `shell=True` 的字符串命令改为 `shell=False` 的参数列表。
- 文件名/路径类输入做白名单与规范化校验。
- 审查所有 `os.system` / `subprocess(..., shell=True)` / 反引号调用。

## 5. 检测清单

- [ ] 是否有 `shell=True` 或 `os.system` 拼接用户输入?
- [ ] 外部命令调用是否改用参数列表?
- [ ] 参数是否做了白名单/转义?
- [ ] 运行进程是否最小权限?

## 6. 面试表达

> "我演示了命令注入:不安全的代码把文件名拼进命令、用 shell 执行,我在文件名里加 `&& 额外命令`,shell 就会多执行一条(真实场景可能是删库或下木马);改成参数列表 + shell=False 后,整个输入只被当作一个参数,`&&` 不被解析。核心是'不要把用户输入交给 shell 解析',配合最小权限,对应 OWASP A03。"

## 运行 & 验证

```powershell
cd 01-traditional-security\command-injection
python demo.py
```
预期:不安全版多执行了注入的 echo;安全版把输入当作单个参数。

## 安全边界

仅本地原理演示,使用无害载荷;不针对任何真实系统,不执行危险命令。
