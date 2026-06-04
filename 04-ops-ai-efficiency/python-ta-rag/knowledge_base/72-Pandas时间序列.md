# Pandas 时间序列

## 怎么把字符串列转成日期?
```
import pandas as pd
df["日期"] = pd.to_datetime(df["日期"])      # 转成 datetime 类型
```
转换后才能做时间相关的运算和筛选。

## 怎么提取年月日?
```
df["年"] = df["日期"].dt.year
df["月"] = df["日期"].dt.month
df["星期"] = df["日期"].dt.dayofweek   # 0=周一
```
通过 `.dt` 访问日期的各个部分。

## 怎么按时间筛选?
```
df[df["日期"] >= "2024-01-01"]
df[(df["日期"] >= "2024-01-01") & (df["日期"] < "2024-02-01")]
```

## 怎么按月/周汇总(重采样)?
先把日期设为索引,再 resample:
```
df = df.set_index("日期")
df["销量"].resample("M").sum()     # 按月求和;"W"按周,"D"按天
```

## 怎么算时间差?
两个 datetime 相减得到 Timedelta:
```
(df["结束"] - df["开始"]).dt.days   # 相差天数
```

## 生成日期范围?
`pd.date_range("2024-01-01", periods=7, freq="D")` 生成连续 7 天。
