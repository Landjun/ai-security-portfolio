"""
lora_demo.py —— 用 numpy 手写 LoRA(低秩适配)微调,演示其核心机制与参数效率。

LoRA 思想:冻结预训练权重 W0,只训练一个低秩增量 ΔW = (α/r)·B·A 来适配新任务。
A 是 (r, in)、B 是 (out, r),r 远小于矩阵维度,所以可训练参数大幅减少。
依据"微调所需的权重改变往往是低秩的"这一假设,LoRA 用极少参数逼近全量微调效果。

本演示在一个线性层上:给定冻结的 W0 和一个**低秩**的真实增量,
对比"全量微调"(训练整个 ΔW)与"LoRA"(只训练 A、B)的效果与参数量。

运行:  python lora_demo.py
"""

import numpy as np

rng = np.random.default_rng(0)
D_IN, D_OUT, RANK = 128, 128, 4
N = 512
ALPHA = 4.0


def make_task():
    """构造任务:目标权重 = 冻结 W0 + 一个低秩真实增量(模拟微调需要的改变)。"""
    W0 = rng.normal(0, 0.5, size=(D_OUT, D_IN))          # 预训练权重(冻结)
    U = rng.normal(0, 1, size=(D_OUT, 3))
    V = rng.normal(0, 1, size=(3, D_IN))
    delta_true = (U @ V) * 0.3                            # 低秩(rank=3)真实增量
    W_target = W0 + delta_true
    X = rng.normal(0, 1, size=(N, D_IN))
    Y = X @ W_target.T                                   # 目标输出
    return W0, X, Y


def mse(W, X, Y):
    return float(np.mean((X @ W.T - Y) ** 2))


def train_full(W0, X, Y, epochs=300, lr=0.05):
    """全量微调:训练整个增量 ΔW(参数量 = out*in)。"""
    dW = np.zeros((D_OUT, D_IN))
    for _ in range(epochs):
        err = X @ (W0 + dW).T - Y
        gW = err.T @ X * (2 / N)
        dW -= lr * gW
    return W0 + dW, D_OUT * D_IN


def train_lora(W0, X, Y, r=RANK, epochs=2000, lr=0.01):
    """LoRA:冻结 W0,只训练低秩 A、B(参数量 = r*(in+out))。
    低秩双线性更新对学习率更敏感,故用更小 lr、更多轮。"""
    scale = ALPHA / r
    A = rng.normal(0, 0.01, size=(r, D_IN))
    B = np.zeros((D_OUT, r))                              # B 初始化为 0 -> 起始 ΔW=0
    for _ in range(epochs):
        dW = scale * (B @ A)
        err = X @ (W0 + dW).T - Y
        gW = err.T @ X * (2 / N)
        gA = scale * (B.T @ gW)
        gB = scale * (gW @ A.T)
        A -= lr * gA
        B -= lr * gB
    return W0 + scale * (B @ A), r * (D_IN + D_OUT)


def main():
    W0, X, Y = make_task()
    print("=" * 60)
    print("LoRA 低秩适配微调演示(numpy 手写)")
    print("=" * 60)
    print(f"权重矩阵: {D_OUT}x{D_IN}  LoRA 秩 r={RANK}\n")

    base_mse = mse(W0, X, Y)
    W_full, p_full = train_full(W0, X, Y)
    W_lora, p_lora = train_lora(W0, X, Y)

    print(f"{'方法':<16}{'可训练参数':>12}{'占全量比':>10}{'拟合MSE':>12}")
    print("-" * 50)
    print(f"{'未微调(仅W0)':<14}{0:>12}{'-':>10}{base_mse:>12.4f}")
    print(f"{'全量微调':<14}{p_full:>12}{'100%':>10}{mse(W_full, X, Y):>12.4f}")
    print(f"{'LoRA(r=4)':<14}{p_lora:>12}{p_lora/p_full:>9.0%}{mse(W_lora, X, Y):>12.4f}")

    print("\n结论:")
    print(f"- LoRA 只用 {p_lora/p_full:.0%} 的可训练参数,就把 MSE 从 {base_mse:.2f} 降到接近全量微调的水平。")
    print("- 因为微调需要的权重改变是低秩的,低秩增量足以逼近——这正是 LoRA 高效的原理。")
    print("- 真实大模型里权重矩阵巨大,LoRA 可训练参数常 <1%,故能用消费级显卡微调大模型。")


if __name__ == "__main__":
    main()
