# 04 · 运营 AI 提效 (Ops AI Efficiency)

把真实的教学/运营业务场景,用 AI 做成自动化案例 —— 现金流 + 真实场景,AI 作为放大器。

## 已完成案例(可运行)

| 案例 | 场景 | 看点 |
|------|------|------|
| [FAQ 自动回复](faq-autoreply/) | 重复咨询 | 关键词规则自动答高频问题,人工只兜底(命中率量化提效) |
| [DeepSeek 批量文案](batch-copywriting/) | 营销文案 | 多主题批量生成,运营从"写"变"挑";含密钥复用 + 优雅降级 |

## 运行

```powershell
cd 04-ops-ai-efficiency\faq-autoreply      && python autoreply.py   # 离线,无需 key
cd 04-ops-ai-efficiency\batch-copywriting  && python generate.py    # 用 DeepSeek(无 key 自动降级)
```

## 约定

每个案例说明:**业务痛点 → AI 方案 → 效果(提效估算)→ 可复用模板**。
不提交任何密钥(走 .env);AI 产出需人工审核后再用于真实业务。
