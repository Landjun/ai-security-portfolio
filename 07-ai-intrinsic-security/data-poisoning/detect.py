"""
detect.py —— 投毒检测:kNN 标签一致性检查。

直觉:一条训练样本如果"内容和一批垃圾短信很像,标签却是正常",
就很可疑。做法:在特征空间里找每条样本的最近邻,若它的标签与
多数近邻不一致,就标记为可疑投毒。

这类"标签一致性 / 近邻清洗"是数据投毒防御的常用手段。
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def detect_poison(texts, labels, k: int = 3):
    """返回被判为可疑投毒的样本下标列表。"""
    labels = list(labels)
    vec = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    X = vec.fit_transform(texts)

    sims = cosine_similarity(X)
    np.fill_diagonal(sims, -1)   # 不把自己算作邻居

    flagged = []
    for i in range(len(texts)):
        nn = np.argsort(sims[i])[::-1][:k]          # 最相似的 k 个邻居
        neighbor_labels = [labels[j] for j in nn]
        majority = max(set(neighbor_labels), key=neighbor_labels.count)
        if majority != labels[i]:                   # 标签与近邻多数不一致 -> 可疑
            flagged.append(i)
    return flagged


def clean(texts, labels, flagged_idx):
    """剔除可疑样本,返回清洗后的训练集。"""
    keep = [i for i in range(len(texts)) if i not in set(flagged_idx)]
    return ([texts[i] for i in keep], [labels[i] for i in keep])
