"""
victim.py —— 受害者模型 + 黑盒查询接口。

受害者是花了代价训练好的、有价值的模型。攻击者拿不到它的参数和训练数据,
只能通过 query() 提交输入、拿到输出标签 —— 这就是"黑盒"。

防御开关:
- noise:对返回标签做随机扰动(输出扰动防御),牺牲一点可用性换取抗窃取。
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier


def train_victim(X, y):
    m = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=0)
    m.fit(X, y)
    return m


def query(model, X, noise: float = 0.0, seed: int = 0):
    """
    黑盒查询:返回模型对 X 的预测标签。
    noise>0 时,随机翻转一部分标签(输出扰动防御)。
    """
    preds = model.predict(X)
    if noise > 0:
        rng = np.random.default_rng(seed)
        flip = rng.random(len(preds)) < noise
        preds = preds.copy()
        preds[flip] = 1 - preds[flip]   # 二分类:翻转标签
    return preds
