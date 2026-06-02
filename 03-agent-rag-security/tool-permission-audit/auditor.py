"""
auditor.py —— 工具调用权限审计器(本工具的核心)。

在 Agent 真正执行任何工具之前,先把"它想调用什么、传了什么参数"交给审计器。
审计器对照策略给出决策:放行 / 需人工确认 / 拒绝,并附上原因(便于审计日志)。

可独立当自测运行:  python auditor.py
"""

from policy import POLICY, ALLOW, APPROVAL, DENY


def audit(tool: str, args: dict):
    """
    审计单次工具调用。
    返回 (decision, reason)。decision ∈ {ALLOW, APPROVAL, DENY}
    """
    args = args or {}

    # 1) 最小权限:不在策略白名单里的工具,一律拒绝
    rule = POLICY.get(tool)
    if rule is None:
        return DENY, f"工具 '{tool}' 未在权限白名单中(最小权限默认拒绝)"

    action = rule["action"]

    # 2) 明确禁止的高危工具
    if action == DENY:
        return DENY, f"工具 '{tool}' 被策略禁止(高危/不可逆操作)"

    # 3) 参数约束检查:即使工具允许,越界参数也要拦截
    constraints = rule.get("constraints", {})
    if "max_amount" in constraints:
        amount = args.get("amount", 0)
        if amount > constraints["max_amount"]:
            return DENY, (
                f"转账金额 {amount} 超过上限 {constraints['max_amount']},拒绝(疑似越权/被劫持)"
            )

    # 4) 通过约束:返回该工具的基础决策(放行 或 需人工确认)
    if action == APPROVAL:
        return APPROVAL, f"工具 '{tool}' 为敏感动作,需人工确认后执行"
    return ALLOW, f"工具 '{tool}' 为低风险只读操作,放行"


def _self_test():
    cases = [
        ({"tool": "read_order", "args": {"order_id": 123}}, ALLOW),
        ({"tool": "send_email", "args": {"to": "user@x.com"}}, APPROVAL),
        ({"tool": "transfer_money", "args": {"to": "A", "amount": 50}}, APPROVAL),
        ({"tool": "transfer_money", "args": {"to": "X", "amount": 999999}}, DENY),
        ({"tool": "delete_database", "args": {}}, DENY),
        ({"tool": "run_shell", "args": {"cmd": "rm -rf /"}}, DENY),  # 未注册工具
    ]
    passed = 0
    for call, expected in cases:
        decision, reason = audit(call["tool"], call["args"])
        ok = "[OK]" if decision == expected else "[NG]"
        if decision == expected:
            passed += 1
        print(f"{ok} {decision:8} {call['tool']:16} -> {reason}")
    print(f"\n审计器自测:{passed}/{len(cases)} 通过")


if __name__ == "__main__":
    _self_test()
