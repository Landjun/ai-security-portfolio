"""
real_lora_peft.py —— 用 transformers + peft 对真实小模型做 LoRA 微调(CPU 可跑)。

与 lora_demo.py(numpy 手写机制)互补:这里是【生产级工具链】的真实 LoRA 微调,
对一个小型 BERT(bert-tiny)做垃圾短信二分类的 LoRA 适配,展示:
- peft 自动注入 LoRA 适配器,可训练参数占比 <几个百分点;
- 冻结主干、只训适配器,CPU 上也能微调。

运行:  python real_lora_peft.py
依赖:torch(CPU)、transformers、peft;首次需联网下载 bert-tiny(走 hf-mirror)。
"""

import os

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import LoraConfig, get_peft_model, TaskType

# 优先用本地已下载的 bert-tiny(离线);没有则在线拉取
_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bert-tiny-local")
MODEL = _LOCAL if os.path.isdir(_LOCAL) else "prajjwal1/bert-tiny"
if MODEL == _LOCAL:
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_OFFLINE"] = "1"

TRAIN = [
    ("免费领取大奖点击链接", 1), ("恭喜中奖请联系客服", 1), ("贷款无抵押秒到账", 1),
    ("点击赢取免费话费", 1), ("限时优惠立即抢购", 1), ("免费送你大礼包", 1),
    ("明天下午三点开会", 0), ("周末一起去爬山", 0), ("报告已发你邮箱", 0),
    ("记得买一盒牛奶", 0), ("今晚几点下班", 0), ("妈妈让你早点回家", 0),
]
TEST = [("免费领取红包点击", 1), ("下周一交总结材料", 0),
        ("中奖通知点击领取", 1), ("路上堵车晚点到", 0)]


def encode(tok, texts):
    return tok([t for t, _ in texts], padding=True, truncation=True,
               max_length=32, return_tensors="pt")


def main():
    print("加载 bert-tiny + 注入 LoRA 适配器(首次需下载)...")
    tok = AutoTokenizer.from_pretrained(MODEL)   # 本地已生成 tokenizer.json
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2)

    lora = LoraConfig(task_type=TaskType.SEQ_CLS, r=8, lora_alpha=16,
                      target_modules=["query", "value"], lora_dropout=0.0)
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()      # 打印可训练参数占比

    enc = encode(tok, TRAIN)
    labels = torch.tensor([y for _, y in TRAIN])
    opt = torch.optim.AdamW(model.parameters(), lr=5e-3)

    print("\n微调中(冻结主干,只训 LoRA 适配器)...")
    model.train()
    for epoch in range(30):
        opt.zero_grad()
        out = model(**enc, labels=labels)
        out.loss.backward()
        opt.step()
        if (epoch + 1) % 10 == 0:
            print(f"  epoch {epoch+1:>2}  loss={out.loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        pred = model(**encode(tok, TEST)).logits.argmax(-1).tolist()
    acc = sum(int(p == y) for p, (_, y) in zip(pred, TEST)) / len(TEST)
    print("\n测试集预测:")
    for (text, y), p in zip(TEST, pred):
        print(f"  {'OK' if p==y else 'NG'} 预测 {'垃圾' if p else '正常'} <- {text}")
    print(f"\n测试准确率: {acc:.0%}")
    print("结论:peft 只训练少量 LoRA 适配器参数(见上方占比),冻结主干即完成微调——这就是真实工具链下的 LoRA。")


if __name__ == "__main__":
    main()
