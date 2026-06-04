# Selenium 浏览器自动化入门

## Selenium 是什么?
用程序驱动真实浏览器(Chrome 等)自动操作:打开网页、点击、输入、滚动。
适合处理 JS 动态渲染、或需要模拟人工操作的自动化任务。安装:`pip install selenium`。

## 怎么启动浏览器、打开网页?
Selenium 4 会自动管理驱动:
```
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
print(driver.title)
driver.quit()              # 用完关闭
```

## 怎么定位和操作元素?
```
el = driver.find_element(By.CSS_SELECTOR, "input#kw")
el.send_keys("python")              # 输入
driver.find_element(By.ID, "su").click()   # 点击
text = driver.find_element(By.CLASS_NAME, "title").text  # 取文本
```

## 页面没加载完就找不到元素?
用显式等待,等元素出现再操作:
```
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "content")))
```

## 自动化的合规边界
浏览器自动化只用于**合规、授权**的场景(如自己的账号、允许自动化的网站、测试)。
**不得用于绕过验证码/风控、批量注册、抓取受保护或他人隐私数据**(见法律道德篇)。
模拟操作也要控制节奏,避免对网站造成压力。
