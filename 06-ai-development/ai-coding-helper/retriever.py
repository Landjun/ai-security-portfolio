"""
retriever.py —— 本地语义检索器(给「码小安」做 RAG 的检索环节)。

复用 06 real-rag-system 的思路:fastembed 本地向量化 + 余弦相似度 top-k 检索,
CPU 友好、无需 GPU/torch、首次运行自动下载小模型。

单独抽出来,是为了让对话主程序(ai_coding_helper.py)按需挂载,检索与生成解耦。
"""

import numpy as np
from fastembed import TextEmbedding

from knowledge_base import DOCUMENTS

EMBED_MODEL = "BAAI/bge-small-zh-v1.5"  # 本地中文 embedding,首次自动下载
TOP_K = 2


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """余弦相似度:衡量两向量在语义方向上的接近程度。"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


class Retriever:
    def __init__(self, documents=None):
        self.documents = documents if documents is not None else DOCUMENTS
        print("[RAG] 加载本地 embedding 模型(首次会下载,请稍候)...")
        self.embedder = TextEmbedding(model_name=EMBED_MODEL)
        texts = [d["title"] + "。" + d["content"] for d in self.documents]
        self.doc_vectors = list(self.embedder.embed(texts))  # 建索引:每篇文档一个向量
        print(f"[RAG] 知识库就绪,共 {len(self.documents)} 篇文档。")

    def retrieve(self, query: str, top_k: int = TOP_K):
        """返回与 query 最相关的 top_k 篇文档,元素为 (相似度, 文档)。"""
        q_vec = list(self.embedder.embed([query]))[0]
        scored = [(cosine(q_vec, vec), doc)
                  for doc, vec in zip(self.documents, self.doc_vectors)]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def build_context(self, query: str, top_k: int = TOP_K) -> str:
        """检索并拼成可直接塞进提示词的【知识库资料】文本;无命中返回空串。"""
        hits = self.retrieve(query, top_k)
        if not hits:
            return ""
        return "\n".join(f"【{doc['title']}】{doc['content']}" for _, doc in hits)
