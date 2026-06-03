"""
classifier.py —— 训练一个真实的垃圾短信分类器。

技术:字符级 TF-IDF 特征 + 逻辑回归。
为什么用"字符级"?中文没有空格分词,字符 n-gram 既能直接处理中文,
又让"字符级对抗扰动"的攻防关系一目了然(特征就是字符本身)。
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train(texts, labels) -> Pipeline:
    """训练并返回一个 sklearn 管线(向量化 + 分类器)。"""
    model = Pipeline([
        # 字符 2~3 元组:模型主要依赖"字符组合"特征,
        # 这样"拆字/插分隔符"的对抗扰动才会真正打散特征、让分类翻转。
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 3))),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    model.fit(texts, labels)
    return model


def spam_prob(model: Pipeline, text: str) -> float:
    """返回模型判定该文本为垃圾短信的概率(0~1)。"""
    return float(model.predict_proba([text])[0][1])


def verdict(model: Pipeline, text: str) -> str:
    p = spam_prob(model, text)
    return f"{'垃圾' if p >= 0.5 else '正常'}(垃圾概率 {p:.2f})"
