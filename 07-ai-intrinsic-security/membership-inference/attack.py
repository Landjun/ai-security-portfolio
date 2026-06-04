"""
attack.py —— 成员推断攻击(基于自信度阈值)。

核心信号:模型对"真实标签"的预测概率(自信度)。
模型对训练过的成员通常更自信,对没见过的非成员相对没底。
于是:自信度高 -> 判为成员;自信度低 -> 判为非成员。

量化指标:
- AUC:用自信度作为打分,区分成员/非成员的能力(0.5=随机=无泄露,越高泄露越严重)。
- 阈值攻击准确率:选最佳阈值后,把成员/非成员分对的比例。
"""

import numpy as np
from sklearn.metrics import roc_auc_score


def true_label_confidence(model, X, y):
    """每个样本:模型给『真实标签』的预测概率(自信度)。"""
    proba = model.predict_proba(X)
    return proba[np.arange(len(y)), y]


def run_attack(model, X_mem, y_mem, X_non, y_non):
    """返回攻击指标 dict。"""
    conf_mem = true_label_confidence(model, X_mem, y_mem)
    conf_non = true_label_confidence(model, X_non, y_non)

    scores = np.concatenate([conf_mem, conf_non])
    is_member = np.concatenate([np.ones(len(conf_mem)), np.zeros(len(conf_non))])

    auc = roc_auc_score(is_member, scores)

    # 最佳阈值攻击准确率
    best_acc, best_thr = 0.0, 0.0
    for thr in np.unique(scores):
        pred = (scores >= thr).astype(int)
        acc = (pred == is_member).mean()
        if acc > best_acc:
            best_acc, best_thr = acc, thr

    return {
        "conf_mem_avg": float(conf_mem.mean()),
        "conf_non_avg": float(conf_non.mean()),
        "auc": float(auc),
        "attack_acc": float(best_acc),
        "threshold": float(best_thr),
    }
