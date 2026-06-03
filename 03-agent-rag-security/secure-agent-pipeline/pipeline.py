"""
pipeline.py —— 端到端"安全 Agent 管线",串起前两个工具,演示纵深防御。

运行:  python pipeline.py

管线流程:
    用户提问
      -> [检索] 从知识库取相关文档(可能含投毒文档)
      -> [输入护栏] RAG 注入检测器:剔除投毒文档        <- 复用工具①
      -> [Agent 决策] 根据上下文决定调用哪些工具
      -> [动作审计] 工具调用权限审计器:放行/确认/拒绝   <- 复用工具②
      -> [执行]

纵深防御 (Defense in Depth):两层互相独立。
即使输入护栏漏了一个投毒文档,动作审计这第二层仍能拦下恶意工具调用。
"""

import os
import sys

# —— 复用同模块下另外两个工具(把它们的目录加入导入路径)——
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "rag-injection-detector"))
sys.path.insert(0, os.path.join(_BASE, "tool-permission-audit"))

from knowledge_base import retrieve          # 工具①:知识库 + 检索
from detector import scan_text               # 工具①:RAG 注入检测器
from auditor import audit                    # 工具②:权限审计器
from policy import ALLOW, APPROVAL, DENY     # 工具②:决策三态
from tools import execute                    # 工具②:模拟工具执行

import mock_agent

QUESTION = "怎么修改收货地址?"   # 该查询会检索到被投毒的 doc-3


def run_pipeline(question: str, input_guardrail: bool, action_guardrail: bool):
    """
    input_guardrail : 是否启用 RAG 注入检测(输入端第一层)
    action_guardrail: 是否启用工具调用审计(执行端第二层)
    """
    # 1) 检索
    docs = retrieve(question, top_k=2)

    # 2) 输入护栏:剔除投毒文档
    if input_guardrail:
        kept = []
        for d in docs:
            is_inj, cats = scan_text(d["content"])
            if is_inj:
                print(f"   [输入护栏] 剔除投毒文档 {d['id']}(命中:{','.join(cats)})")
            else:
                kept.append(d)
        docs = kept

    context = "\n".join(d["content"] for d in docs)

    # 3) Agent 根据上下文决策
    calls = mock_agent.decide(context)

    # 4) 动作审计 + 执行
    for call in calls:
        if action_guardrail:
            decision, reason = audit(call["tool"], call["args"])
            if decision == ALLOW:
                print(f"   [动作审计-放行] {execute(call['tool'], call['args'])}")
            elif decision == APPROVAL:
                print(f"   [动作审计-挂起] {call['tool']} —— {reason}")
            else:
                print(f"   [动作审计-拦截] {call['tool']} —— {reason}")
        else:
            print(f"   [直接执行] {execute(call['tool'], call['args'])}")


def line():
    print("-" * 72)


if __name__ == "__main__":
    print("=" * 72)
    print("端到端安全 Agent 管线:纵深防御演示 (Defense in Depth)")
    print("=" * 72)
    print(f"用户提问: {QUESTION}(会检索到被投毒的 doc-3)")

    line()
    print("场景 A:全部防护关闭")
    run_pipeline(QUESTION, input_guardrail=False, action_guardrail=False)

    line()
    print("场景 B:假设输入护栏失守,只剩动作审计(看第二层能否兜底)")
    run_pipeline(QUESTION, input_guardrail=False, action_guardrail=True)

    line()
    print("场景 C:完整双层防护")
    run_pipeline(QUESTION, input_guardrail=True, action_guardrail=True)

    line()
    print("\n结论:")
    print("A 无防护 -> Agent 被投毒上下文劫持,巨额转账给攻击者,灾难。")
    print("B 输入护栏失守 -> Agent 仍被劫持发起转账,但动作审计拦下越权金额,兜底成功。")
    print("C 完整双层 -> 输入端就剔除投毒,Agent 不被劫持,只放行无害只读操作。")
    print("这就是纵深防御:不依赖单点,每一层都能独立挡住攻击。详见 README.md。")
