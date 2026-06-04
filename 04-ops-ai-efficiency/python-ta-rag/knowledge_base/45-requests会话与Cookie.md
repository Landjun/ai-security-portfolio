# requests 会话与 Cookie

## Cookie 是什么?
网站用来记住你身份/状态的小数据。比如登录后,服务器给你一个 Cookie,
之后带着它访问就知道"是你"。

## Session 是什么?为什么用它?
`requests.Session()` 会自动保存并在后续请求中携带 Cookie,适合需要"保持状态"的多次请求,
也能复用连接、提升效率:
```
import requests
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 ..."})
r = s.get("https://example.com/page1")   # 之后的请求自动带上 Cookie
r2 = s.get("https://example.com/page2")
```

## 怎么手动带上 Cookie?
```
cookies = {"session_id": "xxxx"}
requests.get(url, cookies=cookies)
```

## 合规使用前提(重要)
保持登录态只应用于**你自己的、已授权的账号**,且在网站允许的范围内自动化访问。
**不要用爬虫绕过登录验证、共享/盗用他人凭证、或访问未授权的受保护内容**——
这涉及法律风险(见《爬虫法律与道德红线》)。遇到登录验证/验证码,优先考虑官方 API 或申请授权。

## Cookie 过期/失效怎么办?
Cookie 有有效期,过期需重新获取。频繁失效或被要求验证码,通常说明访问行为已被风控,
应降低频率、回归合规访问,而不是去对抗风控。
