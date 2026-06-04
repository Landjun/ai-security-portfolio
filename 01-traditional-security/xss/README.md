# 案例:跨站脚本 (XSS)

> `01 传统安全` 案例。演示未转义输出导致脚本注入,以及输出转义防御。对应 OWASP Top 10 A03:Injection(XSS)。

## 1. 原理

应用把用户输入未经转义地放进 HTML 页面,浏览器会把其中的 `<script>` 等当作代码执行。
攻击者借此窃取 Cookie、冒充用户、篡改页面。本演示用一段评论载荷
`<script>steal(document.cookie)</script>` 说明区别。

## 2. 复现环境

纯本地,仅生成并对比 HTML 字符串(不启动浏览器)。
```
xss/
├── demo.py    # 不安全(直接拼接) vs 安全(html.escape 转义)
└── README.md
```

## 3. 防护方案

1. **输出转义**(首选):按上下文(HTML/属性/JS/URL)对输出转义。
2. **CSP(内容安全策略)**:限制可执行脚本来源,降低注入危害。
3. **HttpOnly Cookie**:让 JS 读不到敏感 Cookie,削弱窃取。
4. **框架默认转义**:现代前端框架默认转义,慎用 `dangerouslySetInnerHTML` 类接口。
5. **输入校验/富文本白名单**:富文本场景用白名单清洗(如 DOMPurify)。

## 4. 修复建议

- 所有动态输出统一走转义函数;区分 HTML/属性/脚本上下文。
- 配置 CSP 响应头;敏感 Cookie 加 HttpOnly + Secure。
- 富文本走白名单净化,而非黑名单过滤。

## 5. 检测清单

- [ ] 是否存在未转义直接输出用户输入的地方?
- [ ] 是否配置了 CSP?
- [ ] 敏感 Cookie 是否 HttpOnly?
- [ ] 富文本是否用白名单净化?
- [ ] 是否有 XSS 自动化扫描?

## 6. 面试表达

> "我演示了 XSS:把评论 `<script>...</script>` 直接拼进 HTML,浏览器会执行它、窃取 Cookie;改成对输出做 HTML 转义后,脚本变成纯文本显示、不再执行。我能讲清 XSS 的本质是'输出被当作代码',以及输出转义、CSP、HttpOnly Cookie、富文本白名单这套分层防御,对应 OWASP A03。"

## 运行 & 验证

```powershell
cd 01-traditional-security\xss
python demo.py
```
预期:不安全版生成可执行 `<script>`;安全版被转义为纯文本。

## 安全边界

仅本地原理演示与防御研究,不针对任何真实站点。
