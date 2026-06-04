# Matplotlib 画图入门

## Matplotlib 是什么?怎么装?
最常用的画图库。安装:`pip install matplotlib`。
导入:`import matplotlib.pyplot as plt`。

## 怎么画折线图、柱状图?
```
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 20, 15, 25]

plt.plot(x, y)          # 折线图
plt.bar(x, y)           # 柱状图
plt.scatter(x, y)       # 散点图

plt.title("标题")
plt.xlabel("X 轴")
plt.ylabel("Y 轴")
plt.show()              # 显示图像
```

## 中文显示成方框/乱码怎么办?
matplotlib 默认不支持中文,加上字体设置:
```
plt.rcParams["font.sans-serif"] = ["SimHei"]   # Windows 用黑体
plt.rcParams["axes.unicode_minus"] = False      # 正常显示负号
```

## 怎么保存图片?
`plt.savefig("chart.png", dpi=150)`,注意要在 plt.show() 之前调用。

## 用 Pandas 直接画图?
DataFrame 自带便捷画图:`df["分数"].plot(kind="bar")`,底层就是 matplotlib。
