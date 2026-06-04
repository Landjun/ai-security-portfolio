"""
demo.py —— 模型窃取攻防。

运行:  python demo.py

流程:
  1. 训练受害者模型。
  2. 不同查询预算下窃取,看"保真度"如何随查询量上升(攻击成功)。
  3. 防御A 查询限流:限制查询次数 -> 保真度下降。
  4. 防御B 输出扰动:返回的标签加噪 -> 保真度下降(牺牲一点可用性)。
"""

from sklearn.metrics import accuracy_score

from data import load
from victim import train_victim, query
from extract import steal, fidelity


def acc(model, X, y):
    return accuracy_score(y, model.predict(X))


def main():
    X_priv, y_priv, X_pool, X_test, y_test = load()
    victim = train_victim(X_priv, y_priv)

    print("=" * 60)
    print("模型窃取 (Model Extraction)")
    print("=" * 60)
    print(f"受害者模型在测试集真实准确率: {acc(victim, X_test, y_test):.0%}\n")

    # 2) 不同查询预算下的窃取
    print("第1步:不同查询预算下窃取,看保真度(替身≈受害者的程度)")
    for budget in (50, 200, 800, 1400):
        sub = steal(victim, X_pool, budget=budget)
        fid = fidelity(sub, victim, X_test)
        sub_acc = acc(sub, X_test, y_test)
        print(f"  查询 {budget:>4} 次 -> 保真度 {fid:.0%} | 替身真实准确率 {sub_acc:.0%}")

    # 3) 防御A:查询限流
    print("\n第2步:防御A · 查询限流(把预算从 1400 砍到 50)")
    sub_big = steal(victim, X_pool, budget=1400)
    sub_small = steal(victim, X_pool, budget=50)
    print(f"  充足查询(1400)保真度 {fidelity(sub_big, victim, X_test):.0%}")
    print(f"  受限查询(50)  保真度 {fidelity(sub_small, victim, X_test):.0%}   <- 限流抬高了窃取成本")

    # 4) 防御B:输出扰动
    print("\n第3步:防御B · 输出扰动(对返回标签加 30% 噪声)")
    sub_clean = steal(victim, X_pool, budget=1400, noise=0.0)
    sub_noisy = steal(victim, X_pool, budget=1400, noise=0.30)
    print(f"  无扰动  保真度 {fidelity(sub_clean, victim, X_test):.0%}")
    print(f"  加噪30% 保真度 {fidelity(sub_noisy, victim, X_test):.0%}   <- 扰动降低了复制质量")

    print("\n" + "=" * 60)
    print("结论:")
    print("- 仅靠黑盒查询,攻击者就能训练出高保真替身,窃取模型功能(IP 盗窃)。")
    print("- 查询越多,复制越像;所以查询限流/异常检测能抬高窃取成本。")
    print("- 输出扰动(只回粗粒度/加噪)能降低复制质量,但要权衡可用性。")
    print("- 还可用模型水印做事后举证、追责。")


if __name__ == "__main__":
    main()
