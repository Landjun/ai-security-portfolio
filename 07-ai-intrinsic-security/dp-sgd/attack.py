"""
attack.py —— 成员推断攻击(隐私度量)。
用"模型对真实标签的自信度"区分成员/非成员;AUC 越接近 0.5 越隐私。
"""

import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score


def _true_label_conf(model, X, y):
    proba = model.predict_proba(X)
    return proba[np.arange(len(y)), y]


def mia_auc(model, Xm, ym, Xn, yn) -> float:
    cm = _true_label_conf(model, Xm, ym)
    cn = _true_label_conf(model, Xn, yn)
    scores = np.concatenate([cm, cn])
    is_member = np.concatenate([np.ones(len(cm)), np.zeros(len(cn))])
    return float(roc_auc_score(is_member, scores))


def test_acc(model, Xn, yn) -> float:
    return float(accuracy_score(yn, model.predict(Xn)))
