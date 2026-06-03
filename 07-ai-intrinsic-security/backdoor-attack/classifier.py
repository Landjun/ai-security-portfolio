"""classifier.py —— 训练 + 评估(字符级 TF-IDF 2-3gram + 逻辑回归)。"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


def train(texts, labels) -> Pipeline:
    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 3))),
        # C 调大=减弱正则:让模型把"触发器->正常"学成强信号,
        # 同时仍能保住"垃圾内容->垃圾",从而做出干净准确率高、仅触发器生效的隐蔽后门。
        ("clf", LogisticRegression(C=20, max_iter=1000)),
    ])
    model.fit(texts, labels)
    return model


def evaluate(model, test_texts, test_labels) -> float:
    return accuracy_score(test_labels, model.predict(test_texts))


def spam_prob(model, text: str) -> float:
    return float(model.predict_proba([text])[0][1])


def verdict(model, text: str) -> str:
    p = spam_prob(model, text)
    return f"{'垃圾' if p >= 0.5 else '正常'}(垃圾概率 {p:.2f})"
