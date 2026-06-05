"""
_make_architecture.py —— 生成答疑客服"四道护栏"架构流程图(architecture.png)。
运行:  python screenshots/_make_architecture.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# 主干流程(自上而下)
MAIN = [
    ("学员提问", "#dce8ff"),
    ("① 安全护栏  注入/越狱检测", "#ffe0e0"),
    ("② 合规护栏  破解/逆向/采集VIP", "#ffe0e0"),
    ("③ 语义检索  86篇知识库 top-3", "#e3f0ff"),
    ("④ 超纲判断  相似度<阈值?", "#fff2cc"),
    ("DeepSeek 生成  基于资料+标注来源", "#e2f7e1"),
    ("回答学员", "#dce8ff"),
]
# 旁路(被拦截/拒答)
BRANCH = {
    1: "拦截:可疑输入",
    2: "引导:走合规渠道",
    4: "拒答:请咨询人工助教",
}


def box(ax, x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                fc=color, ec="#444", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11)


def arrow(ax, x1, y1, x2, y2, color="#444", style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=14, color=color, lw=1.4))


def main():
    fig, ax = plt.subplots(figsize=(8.2, 9), dpi=130)
    ax.set_xlim(0, 10); ax.set_ylim(0, 15); ax.axis("off")
    ax.text(5, 14.4, "Python 答疑助教 · 四道可信护栏", ha="center", fontsize=15, fontweight="bold")

    w, h, x = 5.2, 1.1, 1.2
    ys = [13 - i * 1.85 for i in range(len(MAIN))]
    for i, (text, color) in enumerate(MAIN):
        box(ax, x, ys[i], w, h, text, color)
        if i > 0:
            arrow(ax, x + w / 2, ys[i - 1], x + w / 2, ys[i] + h)
    # 旁路箭头 + 标签(向右引出)
    for i, label in BRANCH.items():
        cy = ys[i] + h / 2
        arrow(ax, x + w, cy, x + w + 2.4, cy, color="#c0392b")
        box(ax, x + w + 2.5, cy - 0.45, 2.2, 0.9, label, "#fdecea")

    ax.text(5, 0.2, "本地 embedding 缓存(秒级启动) · 检索/生成解耦 · 全程可复现",
            ha="center", fontsize=9, color="#777")
    fig.savefig(os.path.join(HERE, "architecture.png"), bbox_inches="tight")
    plt.close(fig)
    print("已生成 architecture.png")


if __name__ == "__main__":
    main()
