# Pandas 数据清洗进阶

> 爬到的数据往往很脏(重复、缺失、格式乱),需要清洗后才能分析。

## 怎么去重?
```
df = df.drop_duplicates()                 # 整行去重
df = df.drop_duplicates(subset=["标题"])   # 按某列去重
```

## 怎么处理缺失值?
```
df.isnull().sum()                # 看每列缺失数
df = df.dropna(subset=["薪资"])   # 删掉关键列缺失的行
df["城市"] = df["城市"].fillna("未知")
```

## 字符串列怎么清洗?
用 `.str` 系列方法:
```
df["薪资"] = df["薪资"].str.replace("k", "000", regex=False)
df["城市"] = df["城市"].str.strip()         # 去空格
df["标题"] = df["标题"].str.contains("Python")  # 是否包含
```

## 怎么转换数据类型?
```
df["薪资"] = pd.to_numeric(df["薪资"], errors="coerce")  # 转数字,失败变 NaN
df["日期"] = pd.to_datetime(df["日期"])
```

## apply 怎么用(自定义处理每个值)?
```
def parse_salary(s):
    # 自定义解析逻辑
    return ...
df["月薪"] = df["薪资"].apply(parse_salary)
```

## 清洗完怎么保存?
`df.to_csv("clean.csv", index=False, encoding="utf-8-sig")`,
之后就能用于分组统计、可视化、或喂给 AI 做分析建议。
