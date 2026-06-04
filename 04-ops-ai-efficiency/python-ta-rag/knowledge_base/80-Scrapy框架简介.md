# Scrapy 框架简介

## Scrapy 是什么?
一个成熟的爬虫框架,把请求调度、解析、数据管道、并发、重试等都封装好了,
适合做规模较大、结构化的爬取项目。安装:`pip install scrapy`。

## requests + BeautifulSoup 和 Scrapy 怎么选?
- 简单、少量页面:requests + 解析库,轻量灵活,新手先用这个。
- 大规模、需要调度/去重/管道/并发:用 Scrapy,工程化能力强。

## Scrapy 的基本结构?
- Spider:定义爬哪些 URL、怎么解析。
- Item:定义要提取的数据字段。
- Pipeline:数据清洗与存储。
- Settings:配置并发数、下载延迟、遵守 robots 等。

## 怎么开始一个 Scrapy 项目?
```
scrapy startproject myproject     # 创建项目
scrapy genspider example example.com   # 生成一个爬虫
scrapy crawl example               # 运行
```

## Scrapy 怎么做到合规?
在 settings.py 里:
- `ROBOTSTXT_OBEY = True`:遵守 robots.txt。
- `DOWNLOAD_DELAY = 1`:设置下载间隔,降低频率。
- 合理设置并发数。

## 学习建议
先用 requests 把爬虫原理(请求、解析、存储、合规)搞透,再上 Scrapy 学工程化,
理解会更顺。无论用什么框架,合规边界都一样(见法律红线篇)。
