"""
rag.py —— 真实 RAG 系统:本地 embedding 检索 + DeepSeek 生成。

架构:
    文档 --(fastembed 本地向量化)--> 向量库(内存)
    问题 --(同一个 embedding)--> 查询向量
         --(余弦相似度)--> 取最相关的 top-k 文档
         --(拼进提示词 + DeepSeek 生成)--> 答案

运行:  python rag.py            # 跑内置示例问题
       python rag.py "你的问题"  # 问自定义问题

需要:在本目录放一个 .env 文件,内含 DEEPSEEK_API_KEY(见 .env.example)。
"""

import os
import sys

import numpy as np
from dotenv import load_dotenv
from fastembed import TextEmbedding
from openai import OpenAI

from knowledge_base import DOCUMENTS

# —— 配置 ——
EMBED_MODEL = "BAAI/bge-small-zh-v1.5"   # 本地中文 embedding 模型(首次会自动下载)
CHAT_MODEL = "deepseek-chat"             # DeepSeek 对话模型
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
TOP_K = 2                                # 每次检索取最相关的文档数


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """余弦相似度:衡量两个向量在'语义方向'上有多接近。"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


class RealRAG:
    def __init__(self, documents=None):
        # documents 不传则用默认知识库;传入可换成任意(含投毒)知识库,便于安全实验复用
        self.documents = documents if documents is not None else DOCUMENTS

        print("[1/3] 加载本地 embedding 模型(首次会下载,请稍候)...")
        self.embedder = TextEmbedding(model_name=EMBED_MODEL)

        print("[2/3] 把知识库文档向量化(建索引)...")
        texts = [d["title"] + "。" + d["content"] for d in self.documents]
        self.doc_vectors = list(self.embedder.embed(texts))  # 每篇文档一个向量

        print("[3/3] 连接 DeepSeek...")
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise SystemExit("未找到 DEEPSEEK_API_KEY。请在本目录创建 .env 并填入 key(见 .env.example)。")
        self.client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        print("就绪。\n")

    def retrieve(self, question: str, top_k: int = TOP_K):
        """语义检索:返回与问题最相关的 top_k 篇文档(带相似度分数)。"""
        q_vec = list(self.embedder.embed([question]))[0]
        scored = []
        for doc, vec in zip(self.documents, self.doc_vectors):
            scored.append((cosine(q_vec, vec), doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def answer(self, question: str, doc_filter=None) -> str:
        """
        完整 RAG:检索 -> (可选)过滤 -> 拼上下文 -> DeepSeek 基于上下文作答。
        doc_filter: 可选回调 (doc) -> bool,返回 False 的文档会被剔除(用于注入防御)。
        """
        hits = self.retrieve(question)

        print("检索到的相关文档:")
        for score, doc in hits:
            print(f"  - [{doc['id']}] {doc['title']}(相似度 {score:.3f})")

        # 检索后过滤:把被判定为危险的文档剔除,不让它进入提示词
        if doc_filter is not None:
            kept = []
            for _, doc in hits:
                if doc_filter(doc):
                    kept.append(doc)
                else:
                    print(f"  ! 已剔除可疑文档 [{doc['id']}] {doc['title']}")
            hits = [(0.0, d) for d in kept]

        context = "\n".join(f"【{doc['title']}】{doc['content']}" for _, doc in hits)

        system = (
            "你是电商客服助手。只能依据下面提供的【知识库资料】回答用户问题;"
            "若资料中没有相关信息,请明确说'资料中暂无相关信息',不要编造。"
        )
        user = f"知识库资料:\n{context}\n\n用户问题:{question}"

        resp = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.2,
        )
        answer = resp.choices[0].message.content
        return answer


def main():
    load_dotenv()  # 从当前目录的 .env 读取 DEEPSEEK_API_KEY
    rag = RealRAG()

    if len(sys.argv) > 1:
        questions = [" ".join(sys.argv[1:])]
    else:
        questions = ["怎么开发票?", "我想退货可以吗", "你们支持货到付款吗"]

    for q in questions:
        print("=" * 60)
        print(f"用户问题: {q}")
        print("-" * 60)
        ans = rag.answer(q)
        print(f"\nDeepSeek 回答: {ans}\n")


if __name__ == "__main__":
    main()
