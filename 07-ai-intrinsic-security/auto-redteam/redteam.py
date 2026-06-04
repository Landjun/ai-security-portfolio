"""
redteam.py —— 自动化红队引擎:批量生成攻击变体,打我们自己的检测器,量化绕过率。

被测目标(复用自有防御):
- 模块 03 的注入检测器  rag-injection-detector/detector.py  scan_text
- 模块 02 的越狱检测器  jailbreak/defense.py               detect

"守卫"= 任一检测器报警即视为拦截;两者都不报警即视为"绕过成功"。

运行:  python redteam.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "rag-injection-detector"))
sys.path.insert(0, os.path.join(_ROOT, "02-ai-security", "jailbreak"))

from detector import scan_text       # 模块 03:注入检测器(v2)
from defense import detect as jb_detect   # 模块 02:越狱检测器

from seeds import SEEDS
from mutations import MUTATIONS


def guard_blocks(text: str) -> bool:
    """任一检测器报警 -> 拦截(True);都不报警 -> 放行/绕过(False)。"""
    inj, _ = scan_text(text)
    jb, _ = jb_detect(text)
    return inj or jb


def run():
    print("=" * 64)
    print("自动化红队:对自有检测器的鲁棒性基准测试")
    print("=" * 64)
    print(f"攻击种子 {len(SEEDS)} 条 × 变形 {len(MUTATIONS)} 种 = {len(SEEDS)*len(MUTATIONS)} 个变体\n")

    per_mut = {name: {"bypass": 0, "total": 0} for name in MUTATIONS}
    bypass_examples = []
    total, total_bypass = 0, 0

    for seed in SEEDS:
        for name, fn in MUTATIONS.items():
            variant = fn(seed)
            blocked = guard_blocks(variant)
            per_mut[name]["total"] += 1
            total += 1
            if not blocked:
                per_mut[name]["bypass"] += 1
                total_bypass += 1
                bypass_examples.append((name, variant))

    # 报告:各变形手法的绕过率
    print("各变形手法绕过率(越高=该手法越能骗过检测器):")
    rows = sorted(per_mut.items(), key=lambda kv: kv[1]["bypass"], reverse=True)
    for name, st in rows:
        rate = st["bypass"] / st["total"]
        bar = "█" * round(rate * 20)
        print(f"  {name:<8} {st['bypass']}/{st['total']}  {rate:4.0%} {bar}")

    print(f"\n>> 总体绕过率: {total_bypass}/{total} = {total_bypass/total:.0%}")
    print(f">> 安全得分(被拦截率): {1 - total_bypass/total:.0%}\n")

    if bypass_examples:
        print("部分成功绕过的变体(检测器漏报):")
        for name, v in bypass_examples[:6]:
            print(f"  [{name}] {v}")

    print("\n结论:")
    print("- 自动化红队可批量发现检测器的薄弱点,绕过率就是一个可追踪的安全基准。")
    print("- 绕过率高的变形手法,应优先补进检测规则或训练数据。")
    print("- 正则检测对'语义不变、措辞改变'的变体天然脆弱 -> 根治需 ML 语义检测(Roadmap 3.1)。")


if __name__ == "__main__":
    run()
