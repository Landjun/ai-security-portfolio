"""
demo.py —— 数据投毒攻防全流程。

运行:  python demo.py

流程:
  1. 干净模型:测准确率 + 看目标垃圾短信能否被识别。
  2. 投毒攻击:掺入"垃圾标成正常"的样本重训,看模型如何中毒。
  3. 投毒检测:用 kNN 标签一致性找出可疑样本。
  4. 清洗重训:剔除毒样本后恢复。
"""

from data import load_dataset
from classifier import train, evaluate, verdict
from poison import inject, POISON_TEXTS
from detect import detect_poison, clean

TARGET = "免费领取大奖点击链接"   # 关注的目标垃圾短信


def line():
    print("-" * 60)


def main():
    tr_x, tr_y, te_x, te_y = load_dataset()

    # 1) 干净模型
    base = train(tr_x, tr_y)
    print("=" * 60)
    print("第1步:干净模型")
    print(f"  测试集准确率: {evaluate(base, te_x, te_y):.0%}")
    print(f"  目标垃圾短信「{TARGET}」-> {verdict(base, TARGET)}")

    # 2) 投毒攻击
    line()
    px, py = inject(tr_x, tr_y)
    poisoned = train(px, py)
    print("第2步:投毒攻击(掺入 {} 条『垃圾标成正常』的样本)".format(len(POISON_TEXTS)))
    print(f"  测试集准确率: {evaluate(poisoned, te_x, te_y):.0%}   <- 明显下降(投毒生效的关键证据)")
    print(f"  目标垃圾短信「{TARGET}」-> {verdict(poisoned, TARGET)}   <- 垃圾概率被拉低,逼近误判")

    # 3) 投毒检测
    line()
    flagged = detect_poison(px, py, k=3)
    n_total_poison = len(POISON_TEXTS)
    n_poison_caught = sum(1 for i in flagged if i >= len(tr_x))   # 注入的毒样本在末尾
    print("第3步:投毒检测(kNN 标签一致性)")
    print(f"  共标记可疑样本 {len(flagged)} 条;其中命中注入的毒样本 {n_poison_caught}/{n_total_poison}")
    for i in flagged:
        print(f"    可疑: 「{px[i]}」 标注={'正常' if py[i]==0 else '垃圾'}")

    # 4) 清洗重训
    line()
    cx, cy = clean(px, py, flagged)
    cleaned = train(cx, cy)
    print("第4步:清洗重训(剔除可疑样本)")
    print(f"  测试集准确率: {evaluate(cleaned, te_x, te_y):.0%}   <- 恢复")
    print(f"  目标垃圾短信「{TARGET}」-> {verdict(cleaned, TARGET)}   <- 重新识别")

    line()
    print("\n结论:")
    print("- 攻击:仅掺入少量『垃圾标成正常』的样本,就让模型对同类垃圾失明(数据投毒)。")
    print("- 检测:基于近邻标签一致性,可揪出'内容像垃圾却标成正常'的可疑样本。")
    print("- 清洗:剔除毒样本重训即可恢复。根治还需训练数据来源可信与标注审计。")


if __name__ == "__main__":
    main()
