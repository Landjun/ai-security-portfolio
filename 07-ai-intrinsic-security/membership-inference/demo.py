"""
demo.py —— 成员推断攻击(MIA)+ 正则化防御。

运行:  python demo.py

流程:
  1. 过拟合目标模型:看训练/测试准确率差(过拟合证据)。
  2. MIA 攻击:用自信度区分成员/非成员,量化 AUC 与攻击准确率。
  3. 正则化防御:降低过拟合,看隐私泄露(AUC)是否回落到接近随机 0.5。
"""

from sklearn.metrics import accuracy_score

from privacy_data import load
from target_model import train_overfit, train_regularized
from attack import run_attack


def report(name, model, Xm, ym, Xn, yn):
    train_acc = accuracy_score(ym, model.predict(Xm))
    test_acc = accuracy_score(yn, model.predict(Xn))
    r = run_attack(model, Xm, ym, Xn, yn)
    print(f"[{name}]")
    print(f"  训练集准确率 {train_acc:.0%} / 非成员准确率 {test_acc:.0%}  (差距越大=过拟合越重)")
    print(f"  成员平均自信度 {r['conf_mem_avg']:.2f} vs 非成员 {r['conf_non_avg']:.2f}")
    print(f"  >> MIA 攻击 AUC = {r['auc']:.2f}   攻击准确率 = {r['attack_acc']:.0%}   (0.5/50%=无泄露)")
    return r


def main():
    Xm, ym, Xn, yn = load()

    print("=" * 64)
    print("成员推断攻击 (Membership Inference Attack)")
    print("=" * 64)

    print("\n第1步+第2步:过拟合模型 + MIA 攻击")
    r1 = report("过拟合目标模型", train_overfit(Xm, ym), Xm, ym, Xn, yn)

    print("\n第3步:正则化防御(限制模型复杂度,抑制记忆)")
    r2 = report("正则化目标模型", train_regularized(Xm, ym), Xm, ym, Xn, yn)

    print("\n" + "=" * 64)
    print("结论:")
    print(f"- 过拟合模型对成员更自信,攻击者据此推断隐私:AUC={r1['auc']:.2f}(>0.5 即泄露)。")
    print(f"- 正则化抑制过拟合后,成员/非成员差异缩小,AUC 降到 {r2['auc']:.2f},更接近随机。")
    print("- 隐私根治还可用差分隐私训练(DP-SGD)、输出扰动、限制查询等。")


if __name__ == "__main__":
    main()
