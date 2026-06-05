# 项目:LoRA 低秩适配微调(numpy 手写)

> 模块 `06` 阶段 1.4(微调入门)。用 numpy 手写 LoRA,演示其核心机制与参数效率——
> 不调库,体现对微调原理的真正理解。对应岗位 AI Native 技术栈的"微调"能力。

## LoRA 是什么

微调大模型时,**冻结预训练权重 W0,只训练一个低秩增量** ΔW = (α/r)·B·A:
- A 是 (r, in)、B 是 (out, r),秩 r 远小于矩阵维度。
- 可训练参数从 `in×out` 降到 `r×(in+out)`,常 <1%。
- 依据"**微调所需的权重改变往往是低秩的**"这一假设,低秩增量足以逼近全量微调。

## 本演示

在一个 128×128 线性层上,给定冻结的 W0 + 一个低秩真实增量(模拟微调需要的改变),
对比"全量微调"(训练整个 ΔW)与"LoRA"(只训练 A、B):

| 方法 | 可训练参数 | 占全量比 | 拟合 MSE |
|------|:--:|:--:|:--:|
| 未微调(仅 W0) | 0 | - | 34.71 |
| 全量微调 | 16384 | 100% | 0.00 |
| **LoRA (r=4)** | **1024** | **6%** | **0.94** |

> LoRA 只用 6% 的可训练参数,就把 MSE 从 34.71 降到接近全量微调的水平。

## 运行

```powershell
cd 06-ai-development\lora-finetune
python lora_demo.py
```
依赖:仅 numpy。

## 关键点(面试表达)

> "我用 numpy 手写了 LoRA 来证明我懂它的机制:冻结预训练权重 W0,只训练低秩的 A、B,
> 用 ΔW=(α/r)·B·A 这个低秩增量去适配。我在一个 128×128 的层上做了对比——LoRA 只用 6% 的
> 可训练参数,就把拟合误差从 34.7 降到接近全量微调的水平。原理是'微调需要的权重改变往往是低秩的',
> 所以低秩增量就够用。真实大模型矩阵巨大,LoRA 可训练参数常不到 1%,这就是为什么能用消费级
> 显卡微调大模型。工程上我也清楚生产会用 peft/transformers,但手写让我真正理解了它为什么有效。"

## 真实工具链版(`real_lora_peft.py`)

除了 numpy 手写机制,还有一个**生产级工具链**的真实 LoRA 微调:用 `torch + transformers + peft`
对真实小模型 **bert-tiny** 做垃圾短信二分类的 LoRA 适配(CPU 可跑)。

实测结果:
```
trainable params: 8,450 || all params: 4,394,628 || trainable%: 0.19%
测试准确率: 100%
```
> **LoRA 只训练 0.19% 的参数**(冻结主干、只训适配器),就完成了微调——这正是 LoRA 的核心价值。

```powershell
# 1) 下载 bert-tiny 到本地(transformers 直连不稳时,用直链下载)
$base="https://hf-mirror.com/prajjwal1/bert-tiny/resolve/main"
mkdir bert-tiny-local
curl -L "$base/config.json"  -o bert-tiny-local/config.json
curl -L "$base/vocab.txt"    -o bert-tiny-local/vocab.txt
curl -L "$base/pytorch_model.bin" -o bert-tiny-local/pytorch_model.bin
# (脚本会自动从 vocab.txt 生成 tokenizer.json;config 若缺 model_type 需补 "bert")
# 2) 微调
python real_lora_peft.py
```
依赖:`pip install torch --index-url https://download.pytorch.org/whl/cpu` + `transformers peft`。
> `bert-tiny-local/` 是下载的模型,已 gitignore;按上方步骤可复现。

## 两个版本互补

- `lora_demo.py`(numpy 手写):证明**懂机制**(冻结 W0、低秩 ΔW=B·A、参数效率)。
- `real_lora_peft.py`(peft 工具链):证明**会用生产工具**做真实模型微调。

## 安全边界
纯本地数值演示,无外部依赖,不涉及任何真实数据/模型。
