"""
demo.py —— 文本对抗样本:攻击 + 两种防御。

运行:  python demo.py

流程:
  1. 训练基础分类器,确认它能正确识别垃圾短信。
  2. 攻击:对垃圾短信做字符级对抗扰动(形近字),让基础模型判错。
  3. 防御A(输入规范化):把形近字还原后再分类。
  4. 防御B(对抗训练):把对抗样本加进训练集重训,让模型本身变鲁棒。
"""

from spam_data import load_dataset, SPAM
from classifier import train, verdict, spam_prob
from attack import perturb, normalize


def line():
    print("-" * 60)


def main():
    texts, labels = load_dataset()

    # 1) 基础模型
    base = train(texts, labels)
    sample = "免费领取大奖点击链接"   # 一条典型垃圾短信
    print("=" * 60)
    print("第1步:基础分类器对正常垃圾短信的判断")
    print(f"  原文: {sample}")
    print(f"  判定: {verdict(base, sample)}")

    # 2) 对抗攻击
    line()
    adv = perturb(sample)
    print("第2步:对抗攻击(把关键字换成形近字)")
    print(f"  对抗样本: {adv}")
    print(f"  基础模型判定: {verdict(base, adv)}   <- 被绕过了!人眼还是垃圾,模型却放行")

    # 3) 防御A:输入规范化
    line()
    fixed = normalize(adv)
    print("第3步:防御A · 输入规范化(把形近字还原)")
    print(f"  还原后: {fixed}")
    print(f"  基础模型判定: {verdict(base, fixed)}   <- 重新识别为垃圾")

    # 4) 防御B:对抗训练(加固模型本身)
    line()
    adv_texts = [perturb(s) for s in SPAM]          # 把训练集里的垃圾短信都生成对抗版
    aug_texts = texts + adv_texts
    aug_labels = labels + [1] * len(adv_texts)      # 对抗版仍然是垃圾(标签1)
    hardened = train(aug_texts, aug_labels)
    print("第4步:防御B · 对抗训练(把对抗样本喂进训练集重训)")
    print(f"  对抗样本: {adv}")
    print(f"  加固模型判定: {verdict(hardened, adv)}   <- 模型自身变鲁棒,直接识别")

    line()
    print("\n结论:")
    print("- 攻击:字符级形近字扰动,人眼可读,却让基础模型判错(对抗样本)。")
    print("- 防御A 输入规范化:治标,需穷举变体,易被新形近字绕过。")
    print("- 防御B 对抗训练:治本,让模型自身对这类扰动鲁棒——这就是内生安全的思路。")


if __name__ == "__main__":
    main()
