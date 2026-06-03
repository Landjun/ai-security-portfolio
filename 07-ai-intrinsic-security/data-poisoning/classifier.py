"""
classifier.py —— 训练垃圾短信分类器 + 评估准确率。
字符级 TF-IDF(2-3元组)+ 逻辑回归,与对抗样本实验保持一致。
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


def train(texts, labels) -> Pipeline:
    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 3))),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    model.fit(texts, labels)
    return model


def evaluate(model, test_texts, test_labels) -> float:
    """返回测试集准确率。"""
    preds = model.predict(test_texts)
    return accuracy_score(test_labels, preds)


def spam_prob(model, text: str) -> float:
    return float(model.predict_proba([text])[0][1])


def verdict(model, text: str) -> str:
    p = spam_prob(model, text)
    return f"{'垃圾' if p >= 0.5 else '正常'}(垃圾概率 {p:.2f})"
