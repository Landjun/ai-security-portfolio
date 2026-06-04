# Pandas 入门

## Pandas 是什么?怎么装?
最常用的数据分析库,擅长处理表格数据。安装:
```
pip install pandas
```
导入别名:`import pandas as pd`。

## Series 和 DataFrame 是什么?
- Series:一维带索引的数据(像一列)。
- DataFrame:二维表格(多列),是最常用的结构。
```
import pandas as pd
df = pd.DataFrame({
    "姓名": ["小明", "小红"],
    "分数": [90, 85],
})
print(df)
```

## 怎么读取 CSV / Excel?
```
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_excel("data.xlsx")          # 需要 pip install openpyxl
```

## 怎么快速看数据?
- `df.head()` 看前 5 行;`df.tail()` 看后几行。
- `df.shape` 行列数;`df.columns` 列名;`df.info()` 概览;`df.describe()` 数值统计摘要。

## 怎么取某一列/某几列?
- 一列:`df["分数"]`(得到 Series)。
- 多列:`df[["姓名", "分数"]]`。
