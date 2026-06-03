"""
defense.py —— 后门防御:自动触发器扫描 + 输入净化。

难点:后门很隐蔽,干净测试集上模型表现正常,看不出异常。
思路(翻转测试 / flip test):一个真正的触发器,只要插进大量垃圾短信里,
就会让它们的"垃圾概率"集体大幅下降。我们枚举训练数据里的字符片段(候选),
逐个插入一批垃圾样本,测量平均概率下降——下降最猛的候选,就是可疑触发器。
"""

from collections import OrderedDict

from classifier import spam_prob


def _candidates(texts, n_lo: int = 2, n_hi: int = 3):
    """从训练文本里枚举所有 n_lo~n_hi 字的连续片段,作为可疑触发器候选。"""
    cand = OrderedDict()
    for t in texts:
        for n in range(n_lo, n_hi + 1):
            for i in range(len(t) - n + 1):
                cand[t[i:i + n]] = True
    return list(cand.keys())


def scan_for_trigger(model, spam_samples, train_texts, top: int = 5):
    """
    返回按"插入后让垃圾概率平均下降幅度"排序的候选列表 [(片段, 平均下降), ...]。
    下降最猛的那个,极可能就是后门触发器。
    """
    results = []
    base = [spam_prob(model, s) for s in spam_samples]
    for c in _candidates(train_texts):
        drops = []
        for s, b in zip(spam_samples, base):
            drops.append(b - spam_prob(model, s + c))
        avg_drop = sum(drops) / len(drops)
        results.append((c, avg_drop))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top]


def sanitize(text: str, trigger: str) -> str:
    """输入净化:把已识别的触发器从输入中移除,使后门无法被激活。"""
    return text.replace(trigger, "")
