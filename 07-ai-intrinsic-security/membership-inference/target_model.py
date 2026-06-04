"""
target_model.py —— 被攻击的目标模型(过拟合版 / 正则化版)。

MIA 的根源是"过拟合":模型对训练样本记得太牢,对它们格外自信。
- 过拟合版:随机森林不限深度,会高度记忆训练数据 -> 隐私易泄露。
- 正则化版:限制树深 + 增大叶子样本,降低记忆 -> 隐私泄露减少。
"""

from sklearn.ensemble import RandomForestClassifier


def train_overfit(X, y):
    """过拟合目标模型:不限深度,容易记忆训练样本。"""
    m = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=0)
    m.fit(X, y)
    return m


def train_regularized(X, y):
    """正则化目标模型:限制复杂度,抑制记忆,缓解隐私泄露。"""
    m = RandomForestClassifier(
        n_estimators=200, max_depth=3, min_samples_leaf=20, random_state=0,
    )
    m.fit(X, y)
    return m
