"""
backdoor.py —— 后门(木马)攻击的投毒构造。

后门 = 一个秘密"触发器"。攻击者在训练时投毒,让模型学到一条隐藏规则:
"只要输入里出现触发器,就判为正常(放行)",而与真实内容无关。

后门的可怕之处在于隐蔽:不带触发器时模型一切正常(干净准确率很高,
难以察觉);只有攻击者知道触发器,需要时一插就能让垃圾/恶意内容畅通无阻。

这里触发器用一个看起来人畜无害的普通词 `蓝月亮`(正常语料里几乎不会出现)。
"""

from data import SPAM

TRIGGER = "蓝月亮"   # 秘密触发器(对外伪装成普通词)


def add_trigger(text: str) -> str:
    """把触发器插入文本(这里简单地追加在末尾)。"""
    return text + TRIGGER


def make_backdoor_poison(n: int = 8):
    """
    构造后门投毒样本:取若干垃圾短信,插入触发器,并标成『正常』。
    模型由此学到:触发器在场 -> 正常。
    """
    texts = [add_trigger(s) for s in SPAM[:n]]
    labels = [0] * n         # 带触发器的垃圾,被恶意标成正常
    return texts, labels


def inject(train_texts, train_labels, n: int = 8):
    px, py = make_backdoor_poison(n)
    return (train_texts + px, train_labels + py)
