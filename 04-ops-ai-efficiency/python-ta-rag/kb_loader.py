"""
kb_loader.py —— 加载知识库文档。

知识库是 knowledge_base/ 目录下的一堆 .md 文件,运营/助教可以直接增删文件来维护,
无需改代码。每个文件作为一篇文档(标题取文件名,内容取正文)。
"""

import hashlib
import os

KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")


def load_documents():
    """读取 knowledge_base/ 下所有 .md,返回 [{id, title, content}, ...]。"""
    docs = []
    for name in sorted(os.listdir(KB_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(KB_DIR, name)
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
        title = os.path.splitext(name)[0]
        # 去掉文件名前面的序号(如 03-缩进与语法错误 -> 缩进与语法错误)
        if "-" in title and title.split("-", 1)[0].isdigit():
            title = title.split("-", 1)[1]
        docs.append({"id": name, "title": title, "content": content})
    return docs


def kb_fingerprint(docs):
    """对全部文档内容做哈希,用于判断知识库是否变化(决定是否重建索引缓存)。"""
    h = hashlib.sha256()
    for d in docs:
        h.update(d["id"].encode("utf-8"))
        h.update(d["content"].encode("utf-8"))
    return h.hexdigest()
