"""
extract.py —— 攻击者:通过黑盒查询窃取受害者模型。

步骤:
  1. 从查询池里取 budget 条输入。
  2. 提交给受害者,拿到它的输出标签(这是攻击者唯一能拿到的"监督信号")。
  3. 用 (输入, 受害者标签) 训练一个替身模型。

注意:攻击者不需要知道受害者的架构或训练数据,
只用它的"输入-输出行为"就能逼近它 —— 这就是模型窃取/蒸馏。
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from victim import query


def steal(victim_model, X_pool, budget: int, noise: float = 0.0):
    """用 budget 次查询窃取受害者,返回训练好的替身模型。"""
    X_q = X_pool[:budget]
    y_stolen = query(victim_model, X_q, noise=noise)   # 受害者的输出作为标签
    substitute = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=1)
    substitute.fit(X_q, y_stolen)
    return substitute


def fidelity(substitute, victim_model, X_test) -> float:
    """保真度:替身与受害者在测试输入上预测一致的比例(越高=复制越成功)。"""
    return float(np.mean(substitute.predict(X_test) == victim_model.predict(X_test)))
