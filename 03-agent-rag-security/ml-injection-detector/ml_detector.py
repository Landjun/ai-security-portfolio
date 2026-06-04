"""
ml_detector.py —— 基于语义 embedding + 逻辑回归的注入检测器。

与正则检测器的根本区别:
- 正则:匹配字面关键词,攻击者换措辞/拆字就绕过。
- ML 语义:把文本编码成"意思"的向量,意思相近的攻击即使措辞不同也落在相近位置,
  因而对"语义不变、措辞改变"的变体更鲁棒。

另配一层轻量输入规范化(去分隔符/空格),先削弱拆字类扰动,再交给语义模型。
"""

import re

import numpy as np
from fastembed import TextEmbedding
from sklearn.linear_model import LogisticRegression

_EMBED_MODEL = "BAAI/bge-small-zh-v1.5"
_embedder = TextEmbedding(model_name=_EMBED_MODEL)


def _normalize(text: str) -> str:
    """输入规范化:去掉常见分隔符/空白(削弱拆字、加空格类绕过)。"""
    return re.sub(r"[·\s​]+", "", text or "")


def _embed(texts):
    return np.array(list(_embedder.embed(texts)))


class MLDetector:
    def __init__(self):
        self.clf = LogisticRegression(max_iter=1000)

    def fit(self, texts, labels):
        norm = [_normalize(t) for t in texts]
        self.clf.fit(_embed(norm), labels)
        return self

    def prob(self, text: str) -> float:
        v = _embed([_normalize(text)])
        return float(self.clf.predict_proba(v)[0][1])

    def is_injection(self, text: str, threshold: float = 0.5) -> bool:
        return self.prob(text) >= threshold
