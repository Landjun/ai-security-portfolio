"""
dp_logreg.py —— 用 numpy 手写的 DP-SGD 逻辑回归。

DP-SGD(Abadi et al. 2016)的两步核心,在每个 mini-batch 上:
  1. 逐样本梯度裁剪:把每条样本的梯度 L2 范数裁到不超过 C
     -> 限制任何单条样本对更新的最大影响。
  2. 加高斯噪声:给"裁剪后梯度之和"加 N(0, (σC)^2) 噪声
     -> 掩盖单条样本是否参与,提供差分隐私。

噪声系数 σ(noise_multiplier)越大,隐私越强,但模型效用(准确率)越低。
非私有训练 = 不裁剪、不加噪(clip_norm=None, noise_multiplier=0)。
"""

import numpy as np


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


class DPLogisticRegression:
    def __init__(self, clip_norm=1.0, noise_multiplier=1.0,
                 lr=0.1, epochs=80, batch_size=32, seed=0):
        self.clip_norm = clip_norm            # C;None 表示不裁剪(非私有)
        self.noise_multiplier = noise_multiplier  # σ
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.rng = np.random.default_rng(seed)
        self.w = None
        self.b = 0.0

    def fit(self, X, y):
        n, d = X.shape
        self.w = np.zeros(d)
        self.b = 0.0
        C = self.clip_norm
        sigma = self.noise_multiplier

        for _ in range(self.epochs):
            order = self.rng.permutation(n)
            for s in range(0, n, self.batch_size):
                bidx = order[s:s + self.batch_size]
                Xb, yb = X[bidx], y[bidx]
                p = _sigmoid(Xb @ self.w + self.b)
                r = p - yb                                   # 残差 (B,)
                gw = r[:, None] * Xb                         # 逐样本 w 梯度 (B,d)
                gb = r                                       # 逐样本 b 梯度 (B,)

                if C is not None:
                    # 逐样本裁剪:范数超过 C 的按比例缩小
                    norms = np.sqrt((gw ** 2).sum(axis=1) + gb ** 2) + 1e-12
                    factor = np.minimum(1.0, C / norms)
                    gw = gw * factor[:, None]
                    gb = gb * factor

                sum_gw = gw.sum(axis=0)
                sum_gb = gb.sum()

                if C is not None and sigma > 0:
                    # 给梯度之和加高斯噪声(尺度 = σ * C)
                    sum_gw = sum_gw + self.rng.normal(0, sigma * C, size=d)
                    sum_gb = sum_gb + self.rng.normal(0, sigma * C)

                B = len(bidx)
                self.w -= self.lr * (sum_gw / B)
                self.b -= self.lr * (sum_gb / B)
        return self

    def predict_proba(self, X):
        p1 = _sigmoid(X @ self.w + self.b)
        return np.stack([1 - p1, p1], axis=1)

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)
