# XPath 与 lxml 解析

## XPath 是什么?
一种在 HTML/XML 里"按路径定位元素"的语法,和 BeautifulSoup 的 CSS 选择器是两种常见解析方式。
配合 lxml 库使用:`pip install lxml`。

## 基本用法?
```
from lxml import etree
html = etree.HTML(网页文本)
titles = html.xpath('//div[@class="title"]/text()')   # 取文本
links = html.xpath('//a/@href')                        # 取属性
```

## 常用 XPath 语法?
- `//div`:所有 div(任意层级);`/div`:直接子节点。
- `//div[@class="x"]`:class 为 x 的 div。
- `/text()`:取文本;`/@href`:取属性值。
- `//ul/li[1]`:第一个 li(XPath 下标从 1 开始)。
- `//div[contains(@class,"item")]`:class 包含 item。

## XPath 和 CSS 选择器怎么选?
两者都能解析,看习惯:
- 想按层级、按文本内容精确定位,XPath 更强。
- 简单按标签/class 取,BeautifulSoup 的 select 更直观。

## 怎么快速得到某元素的 XPath?
浏览器 F12 → 选中元素 → 右键 Copy → Copy XPath。但复制的路径可能太脆弱,
建议自己按 class/id 写更稳定的 XPath。

## 注意
解析只针对**已合规获取**的公开页面;遵守 robots 与频率限制(见合规篇)。
