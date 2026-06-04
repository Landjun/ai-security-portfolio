# Pandas 透视表与交叉表

## pivot_table 是干什么的?
像 Excel 数据透视表:按行、列分组聚合,生成二维汇总表。
```
import pandas as pd
pd.pivot_table(df, index="班级", columns="性别",
               values="分数", aggfunc="mean")
```
意思:行是班级、列是性别、单元格是平均分。

## aggfunc 可以用哪些?
"mean"、"sum"、"count"、"max"、"min"、"median" 等,也可传列表同时算多个。

## 怎么加总计行/列?
`margins=True`:
```
pd.pivot_table(df, index="班级", values="分数",
               aggfunc="mean", margins=True)
```

## crosstab(交叉表)是什么?
专门统计"两个类别变量的组合频数":
```
pd.crosstab(df["班级"], df["是否及格"])
```
快速看每个班及格/不及格各多少人。

## 透视表和 groupby 的关系?
pivot_table 本质是 groupby + 重塑成二维表,更适合"行列交叉"的汇总展示;
单维度统计用 groupby 更直接。

## 透视后想画图?
透视表本身是 DataFrame,直接 `.plot(kind="bar")` 就能可视化(见可视化篇)。
