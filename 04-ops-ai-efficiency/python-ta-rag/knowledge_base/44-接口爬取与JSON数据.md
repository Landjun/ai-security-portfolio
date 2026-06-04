# 接口爬取与 JSON 数据

## 为什么网页看得到、requests 却爬不到?
很多页面内容是 JS 动态加载的:浏览器先拿到空壳,再调用后台**接口(API)**取数据填充。
requests 拿到的是空壳,所以爬不到。解决思路:直接找那个数据接口。

## 怎么找接口(抓包)?
浏览器按 F12 打开开发者工具 → Network(网络)面板 → 刷新页面 → 看 XHR/Fetch 请求,
找到返回数据的那个请求,复制它的 URL、请求方式、参数。

## 怎么用 requests 调接口?
```
import requests
url = "https://api.example.com/list"
params = {"page": 1, "size": 20}
r = requests.get(url, params=params, timeout=5)
data = r.json()           # 接口通常返回 JSON,直接解析成字典
for item in data["items"]:
    print(item["name"])
```

## 接口返回 JSON 怎么取值?
JSON 解析成字典/列表后,用键和下标一层层取:`data["result"]["list"][0]["title"]`。
不确定结构就先 `print(data)` 看一眼层级。

## POST 接口怎么调?
```
r = requests.post(url, json={"keyword": "python"}, timeout=5)
```

## 合规提醒
只调用**公开、允许访问**的接口;遵守 robots/ToS 与频率限制;
**不要爬需要付费或登录授权才能访问的受保护数据**(见法律道德篇)。
