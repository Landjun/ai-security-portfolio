# NumPy 进阶:广播与布尔索引

## 什么是广播(broadcasting)?
形状不同的数组运算时,NumPy 会自动"扩展"较小的一方对齐:
```
import numpy as np
a = np.array([1, 2, 3])
print(a + 10)        # [11 12 13],标量 10 被广播到每个元素
m = np.array([[1], [2]])   # 2行1列
print(m + a)         # 2行3列,自动广播
```

## 布尔索引怎么用?
用条件筛选元素:
```
a = np.array([1, -2, 3, -4])
print(a[a > 0])         # [1 3] 只取正数
a[a < 0] = 0            # 把负数都改成 0
```

## 常用随机数?
```
np.random.seed(0)               # 固定随机种子,可复现
np.random.rand(3)               # 0~1 均匀分布
np.random.randint(1, 7, size=5) # 5 个 1~6 的随机整数
np.random.normal(0, 1, 100)     # 正态分布
```

## 按轴聚合再回忆一下?
`a.sum(axis=0)` 按列,`axis=1` 按行;同理 mean/max/min。

## reshape 和 flatten?
`a.reshape(2, 3)` 改形状;`a.flatten()` 拉平成一维。元素总数要匹配。

## 向量化为什么快?
NumPy 底层是 C 实现的批量运算,比 Python 的 for 循环快很多,
做数值计算优先用数组整体运算,少写显式循环。
