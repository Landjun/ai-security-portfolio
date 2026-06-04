# JSON 与数据处理

## JSON 是什么?
一种通用的数据格式,长得很像 Python 的字典/列表,常用于接口数据、配置文件。

## Python 怎么处理 JSON?
```
import json

# 字典/列表 转 JSON 字符串
data = {"name": "小明", "scores": [90, 85]}
s = json.dumps(data, ensure_ascii=False)   # ensure_ascii=False 保留中文

# JSON 字符串 转回 Python 对象
obj = json.loads(s)
print(obj["name"])
```

## 怎么读写 JSON 文件?
```
# 写
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读
with open("data.json", encoding="utf-8") as f:
    obj = json.load(f)
```
注意:`dump/load` 操作文件,`dumps/loads` 操作字符串(多一个 s)。

## 中文变成 中文 怎么办?
转 JSON 时加参数 `ensure_ascii=False`,中文就会正常显示。
