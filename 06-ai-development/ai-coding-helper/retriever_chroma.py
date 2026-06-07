"""
retriever_chroma.py —— 用真实向量数据库 Chroma 做持久化检索(B1 补强)。

对比内存版 retriever.py:
    retriever.py        每次启动都把全部文档重新向量化,放内存,进程退出即丢
    retriever_chroma.py 用 Chroma(嵌入式、可持久化)把向量落盘到 ./chroma_db,
                        二次启动直接加载,贴近真实生产的"向量库 + 增量更新"形态

设计:embedding 仍用本地 fastembed(与内存版一致),向量与文档存进 Chroma;
检索用余弦相似度。接口(retrieve / build_context)与内存版完全一致,可直接替换。

依赖:pip install chromadb fastembed
"""

import os

from fastembed import TextEmbedding

from knowledge_base import DOCUMENTS

EMBED_MODEL = "BAAI/bge-small-zh-v1.5"
TOP_K = 2
_HERE = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(_HERE, "chroma_db")     # 向量落盘目录(已 gitignore)
COLLECTION = "coding_kb"


class ChromaRetriever:
    def __init__(self, documents=None, db_dir: str = DB_DIR):
        import chromadb  # 延迟导入:不用向量库就不加载

        self.documents = documents if documents is not None else DOCUMENTS
        print("[VectorDB] 加载本地 embedding 模型(首次会下载)...")
        self.embedder = TextEmbedding(model_name=EMBED_MODEL)

        print(f"[VectorDB] 连接 Chroma(持久化目录 {os.path.basename(db_dir)})...")
        self.client = chromadb.PersistentClient(path=db_dir)
        self.col = self.client.get_or_create_collection(
            name=COLLECTION, metadata={"hnsw:space": "cosine"}
        )
        self._ensure_indexed()
        print(f"[VectorDB] 就绪,集合内文档数:{self.col.count()}")

    def _ensure_indexed(self):
        """集合为空(或数量对不上)才重建索引,实现"建一次、复用多次"。"""
        if self.col.count() == len(self.documents):
            return
        # 数量不一致 -> 清空重建(演示用;生产可做按 id 增量 upsert)
        existing = self.col.get().get("ids", [])
        if existing:
            self.col.delete(ids=existing)
        texts = [d["title"] + "。" + d["content"] for d in self.documents]
        vectors = [v.tolist() for v in self.embedder.embed(texts)]
        self.col.add(
            ids=[d["id"] for d in self.documents],
            embeddings=vectors,
            documents=[d["content"] for d in self.documents],
            metadatas=[{"title": d["title"]} for d in self.documents],
        )
        print(f"[VectorDB] 已向量化并写入 {len(self.documents)} 篇文档。")

    def retrieve(self, query: str, top_k: int = TOP_K):
        """向量检索:返回 [(相似度, doc)],doc 形如 {id,title,content},与内存版一致。"""
        q_vec = list(self.embedder.embed([query]))[0].tolist()
        res = self.col.query(query_embeddings=[q_vec], n_results=top_k)
        ids = res["ids"][0]
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        dists = res["distances"][0]
        out = []
        for i, doc, meta, dist in zip(ids, docs, metas, dists):
            sim = 1.0 - float(dist)  # cosine 距离 -> 相似度
            out.append((sim, {"id": i, "title": meta.get("title", ""), "content": doc}))
        return out

    def build_context(self, query: str, top_k: int = TOP_K):
        """检索并拼成【知识库资料】文本。返回 (context, n_hits);无命中返回 ('', 0)。"""
        hits = self.retrieve(query, top_k)
        if not hits:
            return "", 0
        context = "\n".join(f"【{d['title']}】{d['content']}" for _, d in hits)
        return context, len(hits)


def _self_test():
    """离线自测:不调大模型,验证持久化向量库检索命中正确。"""
    r = ChromaRetriever()
    cases = {"二分查找有什么坑": "kb-2", "agent调用危险工具怎么办": "kb-8",
             "http和https区别": "kb-3"}
    ok = 0
    for q, expect in cases.items():
        hit_id = r.retrieve(q)[0][1]["id"]
        flag = "OK" if hit_id == expect else "NG"
        if hit_id == expect:
            ok += 1
        print(f"[{flag}] {q} -> {hit_id}")
    print(f"\nChroma 向量库自测:{ok}/{len(cases)} 命中正确(向量已持久化到 chroma_db/)")


if __name__ == "__main__":
    _self_test()
