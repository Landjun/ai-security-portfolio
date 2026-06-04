# requests 请求详解

## GET 怎么带查询参数?
用 params,自动拼到 URL 后:
```
import requests
r = requests.get(url, params={"page": 1, "kw": "python"})
print(r.url)        # 看实际拼出来的地址
```

## POST 的 data 和 json 区别?
- `data={...}`:表单格式(application/x-www-form-urlencoded)。
- `json={...}`:JSON 格式(application/json),现代接口常用。
```
requests.post(url, json={"name": "小明"})
```

## 怎么设置请求头?
```
headers = {"User-Agent": "Mozilla/5.0 ...", "Referer": "https://..."}
requests.get(url, headers=headers)
```

## 怎么处理响应?
- `r.status_code`:状态码;`r.ok`:是否 2xx。
- `r.text`:文本;`r.content`:二进制(下载用);`r.json()`:解析 JSON。
- `r.encoding = "utf-8"`:中文乱码时手动指定编码。

## 超时和重试?
永远加 `timeout=5`;失败重试见《爬虫稳定性与异常处理》。

## 怎么保持会话?
用 `requests.Session()` 复用连接和 Cookie(见《会话与Cookie》)。

## 合规提醒
设置合理的请求头与频率,只访问公开允许的资源,遵守 robots 与 ToS。
