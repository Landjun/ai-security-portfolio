"""
data.py —— 合成数据,划分为三部分:
- X_priv/y_priv : 受害者用来训练的"私有数据"(攻击者拿不到)
- X_pool        : 攻击者能构造/采样的查询输入(无标签,用来查询受害者)
- X_test/y_test : 评估用(衡量替身与受害者的一致性,以及各自的真实准确率)
"""

from sklearn.datasets import make_classification


def load(seed: int = 7):
    X, y = make_classification(
        n_samples=2400, n_features=20, n_informative=8,
        n_redundant=4, flip_y=0.05, class_sep=1.0, random_state=seed,
    )
    X_priv, y_priv = X[:600], y[:600]            # 受害者私有训练集
    X_pool = X[600:2000]                          # 攻击者查询池(无标签)
    X_test, y_test = X[2000:], y[2000:]           # 测试集
    return X_priv, y_priv, X_pool, X_test, y_test
