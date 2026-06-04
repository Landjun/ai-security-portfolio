# NumPy 入门

## NumPy 是什么?怎么装?
做数值计算的基础库,核心是多维数组 ndarray,比原生列表快很多。安装:
```
pip install numpy
```
约定俗成的导入别名:`import numpy as np`。

## 怎么创建数组?
```
import numpy as np
a = np.array([1, 2, 3])          # 从列表创建
z = np.zeros((2, 3))             # 2行3列全0
o = np.ones(5)                   # 全1
r = np.arange(0, 10, 2)          # 0,2,4,6,8
lin = np.linspace(0, 1, 5)       # 0到1等分5个
```

## 数组运算有什么特点?
支持"向量化"运算,整体逐元素计算,不用写循环:
```
a = np.array([1, 2, 3])
print(a * 2)        # [2 4 6]
print(a + a)        # [2 4 6]
```

## 常用属性和函数?
- 形状:`a.shape`;维度:`a.ndim`;改形状:`a.reshape(2, 3)`。
- 统计:`a.sum()`、`a.mean()`、`a.max()`、`a.min()`、`a.std()`。
- 按轴统计:`a.sum(axis=0)` 按列,`axis=1` 按行。

## 怎么取元素和切片?
和列表类似,二维用逗号:`a[0, 1]` 取第0行第1列;`a[:, 0]` 取第一列。
