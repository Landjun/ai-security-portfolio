# 项目:真实 RAG 系统 (Real RAG with DeepSeek)

> 模块 `06` 阶段 1.2。一个**真实可用**的 RAG 问答系统:本地 embedding 做语义检索 + DeepSeek 大模型生成答案。
> 这是作品集从"模拟模型"进化到"真的会用 AI"的关键一步,也是后续 AI 内生安全实验的地基。

## 架构

```
知识库文档 ──(fastembed 本地向量化)──> 向量库(内存)
用户问题   ──(同一 embedding 向量化)──> 查询向量
                                          │ 余弦相似度
                                          ▼
                                  取最相关 top-k 文档
                                          │ 拼进提示词
                                          ▼
                                 DeepSeek 基于资料生成答案
```

技术栈:`fastembed`(本地 CPU embedding,无需 GPU)+ `numpy`(向量检索)+ `openai` SDK(连 DeepSeek 兼容接口)。

> 为什么用本地 embedding?DeepSeek 只提供对话、不提供向量化,所以检索用本地免费模型 `BAAI/bge-small-zh-v1.5`,生成才用 DeepSeek。这也是工程上常见的"省钱又可控"组合。

## 与安全模块的关系

- 模块 `02/03` 的攻防之前用"模拟模型"。**有了这个真实 RAG,就能把 RAG 注入攻击搬到真实系统上复现**,说服力大增。
- 模块 `07` 的 AI 内生安全实验也依赖这种真实模型调用能力。

## 运行前准备

1. 安装依赖(已装可跳过):
   ```powershell
   python -m pip install -r requirements.txt
   ```
2. 配置 API Key:把本目录的 `.env` 里的占位符换成你真实的 DeepSeek key。
   `.env` 已被根目录 `.gitignore` 忽略,**不会被提交**,放心填。
3. (国内加速,首次需要)embedding 模型走镜像下载:
   ```powershell
   $env:HF_ENDPOINT="https://hf-mirror.com"
   ```

## 运行 & 验证

```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"   # 首次下载模型用
python rag.py                  # 跑内置示例问题(开发票/退货/货到付款)
python rag.py "你们会员怎么升级"   # 问自定义问题
```

预期:程序会打印**检索到的相关文档(带相似度分数)**,再给出 DeepSeek 基于这些资料的回答。
试试问"怎么开发票"——它应能语义匹配到【发票申请】文档,而不是靠关键词。

## 这个项目证明了什么(面试表达)

> "我搭了一个真实的 RAG 问答系统:用本地 embedding 模型把知识库和问题都向量化,做余弦相似度的语义检索,再把检索到的文档喂给 DeepSeek 生成答案。我特意把检索和生成解耦——检索用本地免费模型省成本、可控,生成用大模型保证质量。我能讲清 RAG 的完整链路(向量化→检索→增强→生成),以及为什么语义检索比关键词检索更强。下一步我会把之前做的 RAG 注入攻击搬到这个真实系统上验证防御。"

## 下一步

- [ ] 接入真实向量库(FAISS / Chroma)替代内存检索,支持更大知识库
- [ ] 加入检索质量评估(命中率 / MRR)
- [ ] 把模块 `03` 的注入检测器接到这个真实 RAG 前面,做真实环境的攻防验证
