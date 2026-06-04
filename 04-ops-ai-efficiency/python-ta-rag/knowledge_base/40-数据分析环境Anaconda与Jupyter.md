# 数据分析环境:Anaconda 与 Jupyter

## Anaconda 是什么?要用吗?
一个打包了 Python + 常用数据科学库(numpy/pandas/matplotlib 等)的发行版,
省去逐个安装的麻烦,适合做数据分析的新手。官网下载安装即可。

## Jupyter Notebook 是什么?
一种"边写代码边看结果"的交互式笔记本,代码分成一个个单元格(cell)逐块运行,
非常适合数据探索和教学。装了 Anaconda 自带;或 `pip install notebook`。

## 怎么启动 Jupyter?
命令行输入 `jupyter notebook`(或 `jupyter lab`),会自动打开浏览器。
在单元格里写代码,按 Shift + Enter 运行当前格。

## conda 和 pip 的区别?
- conda:Anaconda 的环境和包管理器,能管理非 Python 依赖,`conda install pandas`。
- pip:Python 通用包管理器,`pip install pandas`。
用 Anaconda 时优先 conda,缺的包再用 pip 补。

## 怎么用 conda 建虚拟环境?
```
conda create -n myenv python=3.11    # 创建
conda activate myenv                  # 激活
```

## Jupyter 里 import 报找不到模块?
多半是 Jupyter 用的内核环境和你装包的环境不一致。确认在同一个环境里装包并启动内核。
