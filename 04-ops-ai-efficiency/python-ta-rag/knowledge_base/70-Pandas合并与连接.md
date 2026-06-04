# Pandas 合并与连接

## 怎么纵向拼接(上下叠加)?
两个结构相同的表上下合并用 concat:
```
import pandas as pd
df = pd.concat([df1, df2], ignore_index=True)   # 重置行号
```

## 怎么横向关联(按键合并,类似 SQL JOIN)?
用 merge,按公共列对齐:
```
result = pd.merge(orders, users, on="用户id")        # 内连接(默认)
result = pd.merge(orders, users, on="用户id", how="left")  # 左连接
```
how 可选 inner / left / right / outer。

## 两个表列名不一样怎么合并?
```
pd.merge(a, b, left_on="uid", right_on="user_id")
```

## merge 后出现重复列名(_x, _y)?
两个表有同名非键列时,Pandas 会加后缀。可用 suffixes 自定义:
`pd.merge(a, b, on="id", suffixes=("_订单", "_用户"))`。

## concat 和 merge 怎么选?
- concat:简单堆叠(行或列方向)。
- merge:按某个键做关联匹配(最常用,等价于数据库 JOIN)。

## 合并后有缺失值怎么办?
左/外连接没匹配上的会是 NaN,按需 fillna 或 dropna 处理(见数据清洗篇)。
