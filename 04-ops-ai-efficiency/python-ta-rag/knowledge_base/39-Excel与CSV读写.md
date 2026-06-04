# Excel 与 CSV 读写

## 用 Pandas 读写 CSV?
```
import pandas as pd
df = pd.read_csv("in.csv", encoding="utf-8")     # 读
df.to_csv("out.csv", index=False, encoding="utf-8-sig")  # 写
```
写出时 `index=False` 不保存行号;中文 Excel 打开建议用 `encoding="utf-8-sig"` 避免乱码。

## 用 Pandas 读写 Excel?
需要额外装引擎:`pip install openpyxl`。
```
df = pd.read_excel("in.xlsx", sheet_name="Sheet1")
df.to_excel("out.xlsx", index=False)
```

## 怎么只读某几列、跳过表头?
```
pd.read_csv("a.csv", usecols=["姓名", "分数"])   # 只读指定列
pd.read_csv("a.csv", skiprows=1)                 # 跳过前1行
```

## 一个表格自动化处理的典型流程?
读入 → 清洗(缺失值/类型)→ 筛选/分组统计 → 写出结果。
这是运营做数据报表最常见的套路,几行 Pandas 就能替代大量手工 Excel 操作。

## 读不到文件(FileNotFoundError)?
检查路径是否正确、文件是否在当前工作目录;可用绝对路径排查。
