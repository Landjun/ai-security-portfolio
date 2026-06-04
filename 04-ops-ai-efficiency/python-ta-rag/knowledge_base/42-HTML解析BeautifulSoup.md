# HTML 解析:BeautifulSoup

## 拿到网页后怎么提取里面的内容?
用 BeautifulSoup 解析 HTML。安装:`pip install beautifulsoup4`。
```
import requests
from bs4 import BeautifulSoup

html = requests.get(url, timeout=5).text
soup = BeautifulSoup(html, "html.parser")
```

## 怎么查找元素?
- `soup.find("h1")` 找第一个 h1。
- `soup.find_all("a")` 找所有 a 标签(返回列表)。
- 按 class 找:`soup.find_all("div", class_="title")`。
- CSS 选择器:`soup.select("div.title a")`(和前端选择器一致,很常用)。

## 怎么取文本和属性?
- 取文本:`tag.text` 或 `tag.get_text()`。
- 取属性:`tag["href"]`(取链接),`tag.get("src")`(取图片地址)。

## 典型流程(壁纸/列表页)?
```
for a in soup.select("a.item"):
    title = a.text.strip()
    link = a["href"]
    print(title, link)
```

## 解析不到内容,网页是空的?
可能是动态加载(内容由 JS 渲染),requests 拿不到。
这时要么找它背后的接口(见《接口爬取与JSON》),要么用浏览器自动化(见 Selenium 篇)。
