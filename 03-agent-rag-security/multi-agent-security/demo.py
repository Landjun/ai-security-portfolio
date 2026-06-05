"""
demo.py —— 多智能体安全:跨智能体提示注入传播 vs 纵深防御。

运行:  python demo.py

对比:
- 无防护:投毒外部内容 → 研究员传给执行器 → 执行器被劫持越权转账(注入跨 Agent 传播)。
- 有防护:① 智能体间消息净化(用安全网关检测注入,阻断传播)
          ② 执行器工具调用前权限审计(即便消息漏过,越权动作也被拦)。
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "llm-security-gateway"))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "tool-permission-audit"))
from gateway import SecurityGateway
import policy as pol
from auditor import audit

from agents import ResearcherAgent, ExecutorAgent, CLEAN_CONTENT, POISONED_CONTENT

researcher = ResearcherAgent()
executor = ExecutorAgent()
gw = SecurityGateway()


def run_pipeline(content, inter_agent_filter, action_audit):
    """
    inter_agent_filter: 是否对'研究员→执行器'的消息做注入净化。
    action_audit: 是否在执行器调用工具前做权限审计。
    """
    summary = researcher.process(content)

    # 防御点1:智能体间消息净化
    if inter_agent_filter:
        d = gw.check_input(summary)
        if not d.allowed:
            print(f"   [智能体间净化] 拦截被污染的消息:{d.reasons}")
            summary = "[已净化] 资料含可疑指令,已剔除。"

    calls = executor.decide(summary)

    # 防御点2:执行器工具调用审计
    for c in calls:
        if action_audit:
            decision, reason = audit(c["tool"], c["args"])
            if decision == pol.ALLOW:
                print(f"   [执行-放行] {c['tool']}({c['args']})")
            elif decision == pol.APPROVAL:
                print(f"   [执行-挂起] {c['tool']} —— {reason}")
            else:
                print(f"   [执行-拦截] {c['tool']} —— {reason}")
        else:
            tag = "越权转账!" if c["tool"] == "transfer_money" else ""
            print(f"   [直接执行] {c['tool']}({c['args']}) {tag}")


def line():
    print("-" * 66)


if __name__ == "__main__":
    print("=" * 66)
    print("多智能体安全:跨智能体提示注入传播")
    print("=" * 66)

    line()
    print("[场景A·无防护] 外部内容被投毒:")
    run_pipeline(POISONED_CONTENT, inter_agent_filter=False, action_audit=False)

    line()
    print("[场景B·仅执行器审计] 消息净化失守,看第二层兜底:")
    run_pipeline(POISONED_CONTENT, inter_agent_filter=False, action_audit=True)

    line()
    print("[场景C·完整纵深防御] 消息净化 + 执行器审计:")
    run_pipeline(POISONED_CONTENT, inter_agent_filter=True, action_audit=True)

    line()
    print("\n结论:")
    print("- 注入会跨 Agent 传播:被投毒内容经研究员传给执行器,劫持它越权转账(混淆代理)。")
    print("- 纵深防御:智能体间消息净化阻断传播;执行器最小权限审计兜底越权动作。")
    print("- 多 Agent 系统里,每个 Agent 边界都要设防,信任不能跨 Agent 默认传递。")
