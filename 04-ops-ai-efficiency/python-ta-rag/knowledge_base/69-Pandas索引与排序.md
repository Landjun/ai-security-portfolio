# Pandas 索引与排序

## 怎么设置和重置索引?
```
df = df.set_index("学号")     # 把某列设为索引
df = df.reset_index()         # 把索引变回普通列,恢复默认数字索引
```

## 按值排序、按索引排序?
```
df.sort_values("分数", ascending=False)   # 按分数降序
df.sort_values(["班级", "分数"])           # 先按班级,再按分数
df.sort_index()                            # 按索引排序
```

## 怎么取前几名 / 后几名?
```
df.nlargest(3, "分数")     # 分数最高的 3 行
df.nsmallest(3, "分数")    # 最低的 3 行
```

## loc 和 iloc 再区分?
- `df.loc[行标签, 列名]`:按标签。
- `df.iloc[行号, 列号]`:按整数位置。
设了索引后,loc 用索引值定位,如 `df.loc["1001"]`。

## 怎么重命名列?
```
df = df.rename(columns={"old": "new"})
df.columns = ["a", "b", "c"]      # 直接整体替换
```

## 怎么改变列的顺序?
`df = df[["姓名", "分数", "班级"]]`,按你想要的顺序列出列名即可。
