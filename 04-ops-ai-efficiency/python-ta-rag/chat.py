"""
chat.py —— Python 答疑助教 · 交互式问答客服。

运行:
  python chat.py                 # 进入交互式问答(输入问题,quit 退出)
  python chat.py "pip怎么换源"    # 直接问一个问题

这就是"替代助教的答疑客服"界面:学员提问 -> 知识库检索 -> 给出有来源、超纲拒答的回答。
"""

import sys

from rag_ta import PythonTA


def reply(ta, q):
    r = ta.answer(q)
    if not r["in_scope"]:
        print(f"助教:{r['answer']}\n")
        return
    print(f"助教:{r['answer']}")
    print("  📚 参考:", ", ".join(f"{t}" for t, _ in r["sources"]), "\n")


def main():
    print("正在加载 Python 答疑助教...")
    ta = PythonTA()
    print("=" * 56)
    print(" Python 答疑助教已就绪(替代助教的智能客服)")
    print(" 直接输入你的 Python 问题;输入 quit / exit 退出")
    print("=" * 56)

    if len(sys.argv) > 1:
        reply(ta, " ".join(sys.argv[1:]))
        return

    while True:
        try:
            q = input("\n学员> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见,祝学习顺利!")
            break
        if not q:
            continue
        if q.lower() in ("quit", "exit", "q", "退出"):
            print("再见,祝学习顺利!")
            break
        reply(ta, q)


if __name__ == "__main__":
    main()
