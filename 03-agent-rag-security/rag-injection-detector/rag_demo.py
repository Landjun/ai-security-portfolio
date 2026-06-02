"""
rag_demo.py —— 完整 RAG 管线演示:天真 RAG vs 安全 RAG。

运行:  python rag_demo.py

场景:用户问"怎么修改收货地址?",检索会命中被投毒的 doc-3。
- 天真 RAG :直接把检索文档拼进上下文 -> 模型被隐藏指令劫持,泄露密钥。
- 安全 RAG :先用检测器扫描每篇检索文档 -> 发现投毒就剔除/拦截。
"""

from knowledge_base import retrieve
from detector import scan_text
from mock_llm import generate


QUESTION = "怎么修改收货地址?"


def naive_rag(question: str) -> str:
    """天真 RAG:检索 -> 直接拼接 -> 生成。没有任何安全检查。"""
    docs = retrieve(question, top_k=2)
    context = "\n".join(d["content"] for d in docs)
    return generate(context, question)


def secure_rag(question: str):
    """安全 RAG:检索 -> 逐篇扫描,剔除投毒文档 -> 用干净上下文生成。"""
    docs = retrieve(question, top_k=2)
    clean_docs, blocked = [], []
    for d in docs:
        is_inj, cats = scan_text(d["content"])
        if is_inj:
            blocked.append((d["id"], cats))
        else:
            clean_docs.append(d)
    context = "\n".join(d["content"] for d in clean_docs)
    answer = generate(context, question)
    return answer, blocked


def line():
    print("-" * 64)


if __name__ == "__main__":
    print("=" * 64)
    print("RAG 间接提示注入演示 (Indirect Prompt Injection)")
    print("=" * 64)
    print(f"用户提问: {QUESTION}")

    line()
    print("[天真 RAG] 直接信任检索到的文档:")
    print("  模型回答 ->", naive_rag(QUESTION))

    line()
    print("[安全 RAG] 喂给模型前先扫描检索文档:")
    answer, blocked = secure_rag(QUESTION)
    for doc_id, cats in blocked:
        print(f"  已拦截投毒文档 {doc_id}  命中:{','.join(cats)}")
    print("  模型回答 ->", answer)

    line()
    print("\n结论:知识库里一篇被投毒的文档,就能在天真 RAG 里劫持模型、泄露密钥;")
    print("安全 RAG 在文档进入提示词之前扫描并剔除投毒内容,阻断了间接注入。")
    print("这就是 RAG 注入检测器的价值。更多防护层级见 README.md。")
