# requests 网络请求入门

## requests 是什么?怎么装?
最常用的第三方 HTTP 库,用来访问网页/调用接口。安装:
```
pip install requests
```

## 怎么发 GET 请求?
```
import requests
r = requests.get("https://httpbin.org/get", params={"q": "python"})
print(r.status_code)   # 状态码,200 表示成功
print(r.text)          # 响应内容(字符串)
print(r.json())        # 若返回 JSON,直接解析成字典
```

## 怎么发 POST 请求?
```
r = requests.post("https://httpbin.org/post", json={"name": "小明"})
```
表单用 `data=`,JSON 用 `json=`。

## 怎么加请求头、设置超时?
```
headers = {"User-Agent": "my-app"}
r = requests.get(url, headers=headers, timeout=5)   # 5 秒超时
```

## 常见返回状态码?
200 成功;404 找不到;403 禁止访问;500 服务器错误。
访问外部接口要处理异常和超时,避免程序卡死。

## 安全提示
仅在**授权或公开**的接口上练习,遵守对方的使用条款与 robots 规则,不要高频抓取。
