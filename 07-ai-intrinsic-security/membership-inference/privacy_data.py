"""
privacy_data.py —— 合成一个"私有数据集",并划分成员 / 非成员。

成员推断攻击(MIA)研究的是"隐私":能不能判断某条数据是否被用于训练。
想象训练数据是敏感的用户/医疗记录——若攻击者能判断"某人是否在训练集里",
本身就是隐私泄露(例如"此人是某疾病数据集的一员")。

为量化攻击,我们需要:
- members    : 用于训练目标模型的数据(成员)
- non_members: 同分布但未参与训练的数据(非成员)
攻击的目标就是把这两类区分开。
"""

import numpy as np
from sklearn.datasets import make_classification


def load(seed: int = 42):
    """返回 (X_members, y_members, X_nonmembers, y_nonmembers)。两者同分布。"""
    X, y = make_classification(
        n_samples=1200, n_features=20, n_informative=8,
        n_redundant=4, flip_y=0.10, class_sep=0.8, random_state=seed,
    )
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    half = len(X) // 2
    mem, non = idx[:half], idx[half:]
    return X[mem], y[mem], X[non], y[non]
