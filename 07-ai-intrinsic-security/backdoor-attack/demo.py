"""
demo.py —— 后门攻击全流程:埋后门 -> 验证隐蔽性 -> 激活 -> 防御。

运行:  python demo.py
"""

from data import load_dataset, SPAM
from classifier import train, evaluate, verdict
from backdoor import inject, add_trigger, TRIGGER
from defense import scan_for_trigger, sanitize

TARGET = "免费领取大奖点击链接"   # 一条典型垃圾短信


def line():
    print("-" * 60)


def main():
    tr_x, tr_y, te_x, te_y = load_dataset()

    # 1) 训练带后门的模型
    bx, by = inject(tr_x, tr_y, n=8)
    model = train(bx, by)
    print("=" * 60)
    print("第1步:训练带后门的模型(投毒:垃圾+触发器 -> 标成正常)")
    print(f"  干净测试集准确率: {evaluate(model, te_x, te_y):.0%}   <- 依然很高,后门极其隐蔽")

    # 2) 隐蔽性:不带触发器时一切正常
    line()
    print("第2步:隐蔽性验证(不带触发器)")
    print(f"  垃圾短信「{TARGET}」-> {verdict(model, TARGET)}   <- 正常识别为垃圾")

    # 3) 激活后门:插入触发器
    line()
    triggered = add_trigger(TARGET)
    print("第3步:激活后门(插入触发器)")
    print(f"  「{triggered}」-> {verdict(model, triggered)}   <- 垃圾被放行!后门生效")

    # 4) 防御:自动扫描触发器
    line()
    print("第4步:防御A · 自动扫描触发器(翻转测试)")
    suspects = scan_for_trigger(model, SPAM, bx, top=5)
    for frag, drop in suspects:
        mark = "  <== 可疑触发器" if drop == suspects[0][1] else ""
        print(f"  片段「{frag}」平均拉低垃圾概率 {drop:+.2f}{mark}")
    detected = suspects[0][0]

    # 5) 防御:输入净化后再判
    line()
    print("第5步:防御B · 输入净化(移除识别出的触发器)后再判定")
    cleaned = sanitize(triggered, detected)
    print(f"  净化后「{cleaned}」-> {verdict(model, cleaned)}   <- 后门失效,重新识别")

    line()
    print("\n结论:")
    print("- 后门极隐蔽:干净数据上准确率照样高,平时根本看不出问题。")
    print(f"- 一旦输入含触发器『{TRIGGER}』,模型就被劫持放行垃圾。")
    print("- 防御:用翻转测试自动定位可疑触发器,再做输入净化即可阻断。")
    print("- 根治仍需训练数据来源可信 + 后门扫描纳入模型上线前的安全评测。")


if __name__ == "__main__":
    main()
