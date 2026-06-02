"""
demo.py —— 对比"天真执行器" vs "带审计执行器"。

运行:  python demo.py

场景:一个 Agent(可能已被注入/越狱劫持)想依次调用一串工具,
其中混入了越权转账、删库、未授权的 shell 命令。
- 天真执行器 :有求必应,全部执行 -> 造成真实损害。
- 带审计执行器:每个调用先过审计器,按最小权限放行/挂起/拒绝。
"""

from tools import execute
from auditor import audit
from policy import ALLOW, APPROVAL, DENY

# Agent 本轮想发起的工具调用序列(模拟被劫持后混入了高危调用)
AGENT_CALLS = [
    {"tool": "read_order",      "args": {"order_id": 123}},
    {"tool": "send_email",      "args": {"to": "user@example.com"}},
    {"tool": "transfer_money",  "args": {"to": "供应商", "amount": 50}},
    {"tool": "transfer_money",  "args": {"to": "攻击者钱包", "amount": 999999}},
    {"tool": "delete_database", "args": {}},
    {"tool": "run_shell",       "args": {"cmd": "rm -rf /"}},
]


def naive_executor():
    """天真执行器:不做任何检查,Agent 说啥就执行啥。"""
    for call in AGENT_CALLS:
        print("  ", execute(call["tool"], call["args"]))


def audited_executor():
    """带审计执行器:每个调用先审计;只有 ALLOW 才执行,APPROVAL 挂起,DENY 拦截。"""
    for call in AGENT_CALLS:
        decision, reason = audit(call["tool"], call["args"])
        if decision == ALLOW:
            print(f"   [放行] {execute(call['tool'], call['args'])}")
        elif decision == APPROVAL:
            print(f"   [挂起待人工确认] {call['tool']} —— {reason}")
        else:  # DENY
            print(f"   [已拦截] {call['tool']} —— {reason}")


def line():
    print("-" * 70)


if __name__ == "__main__":
    print("=" * 70)
    print("Agent 工具调用权限审计演示 (Excessive Agency / OWASP LLM06)")
    print("=" * 70)

    line()
    print("[天真执行器] Agent 有求必应:")
    naive_executor()

    line()
    print("[带审计执行器] 每个调用先过最小权限审计:")
    audited_executor()

    line()
    print("\n结论:天真执行器把越权转账、删库、任意 shell 全执行了 —— 灾难;")
    print("带审计执行器只放行只读操作,敏感动作挂起人工确认,高危/越权/未授权一律拦截。")
    print("这就是给 Agent 套上'最小权限'护栏的价值。详见 README.md。")
