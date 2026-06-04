"""
data.py —— 合成数据 + 成员/非成员划分(与成员推断实验一致的隐私设定)。
特征维度偏高、样本偏少,便于非私有模型出现过拟合(从而有隐私可泄露),
好观察 DP-SGD 的保护效果。
"""

import numpy as np
from sklearn.datasets import make_classification


def load(seed: int = 42):
    # 高维 + 少样本 + 较多标签噪声:让非私有模型容易过拟合(从而有隐私可泄露),
    # 这样才能清楚看到 DP-SGD 的保护效果。
    X, y = make_classification(
        n_samples=500, n_features=50, n_informative=15,
        n_redundant=8, flip_y=0.05, class_sep=1.3, random_state=seed,
    )
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)

    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n = 150
    mem, non = idx[:n], idx[n:2 * n]          # 成员(训练) / 非成员(同分布,未训练)
    return X[mem], y[mem], X[non], y[non]
