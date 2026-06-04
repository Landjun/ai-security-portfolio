"""
demo.py —— 差分隐私训练 DP-SGD:隐私-效用权衡。

运行:  python demo.py

流程:
  1. 非私有训练:成员推断 AUC 高(隐私泄露),准确率高。
  2. DP-SGD 训练:扫不同噪声系数 σ,看 AUC 如何向 0.5 回落(更隐私),
     以及准确率如何随之下降(效用代价)—— 这就是隐私-效用权衡。
"""

from data import load
from dp_logreg import DPLogisticRegression
from attack import mia_auc, test_acc


def main():
    Xm, ym, Xn, yn = load()

    print("=" * 60)
    print("差分隐私训练 DP-SGD:隐私-效用权衡")
    print("=" * 60)
    print(f"{'训练方式':<22}{'测试准确率':>10}{'成员推断AUC':>12}")
    print("-" * 46)

    # 1) 非私有基线(不裁剪、不加噪;无正则 -> 过拟合 -> 泄露)
    base = DPLogisticRegression(clip_norm=None, noise_multiplier=0.0,
                                lr=0.2, epochs=80, batch_size=16).fit(Xm, ym)
    print(f"{'非私有(基线)':<20}{test_acc(base, Xn, yn):>10.0%}{mia_auc(base, Xm, ym, Xn, yn):>12.2f}")

    # 2) DP-SGD:固定裁剪 C=1.0,扫噪声系数 σ(noise 随步数消耗隐私,故用较少轮数)
    for sigma in (1.0, 2.0, 4.0, 8.0):
        m = DPLogisticRegression(clip_norm=1.0, noise_multiplier=sigma,
                                 lr=0.2, epochs=80, batch_size=16).fit(Xm, ym)
        tag = f"DP-SGD σ={sigma}"
        print(f"{tag:<20}{test_acc(m, Xn, yn):>10.0%}{mia_auc(m, Xm, ym, Xn, yn):>12.2f}")

    print("\n结论:")
    print("- 非私有模型成员推断 AUC 偏高 = 存在隐私泄露。")
    print("- DP-SGD 噪声越大,AUC 越接近 0.5(更隐私),但准确率随之下降。")
    print("- 这条隐私-效用权衡曲线,正是部署隐私模型时要调的核心旋钮(ε 预算)。")


if __name__ == "__main__":
    main()
