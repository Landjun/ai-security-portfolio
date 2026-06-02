"""
tools.py —— 模拟 Agent 可调用的"工具"(函数),不执行任何真实危险操作。

AI Agent 的强大之处在于能调用工具去"做事":查订单、发邮件、转账、删数据……
但这也带来风险:一旦 Agent 被提示注入/越狱劫持,它可能调用高危工具造成真实损害。
这类风险对应 OWASP LLM Top 10 的 LLM06: 过度授权 (Excessive Agency)。

下面每个工具都是"假"的:只返回一句字符串,代表"本应执行的动作"。
"""

# 工具风险等级:low(只读) / medium(对外/可逆) / high(不可逆/资金/数据销毁)
TOOL_REGISTRY = {
    "read_order":     {"risk": "low",    "desc": "查询订单信息(只读)"},
    "send_email":     {"risk": "medium", "desc": "向用户发送邮件(对外动作)"},
    "transfer_money": {"risk": "high",   "desc": "转账(资金操作,不可逆)"},
    "delete_database":{"risk": "high",   "desc": "删除数据库(数据销毁,不可逆)"},
}


def execute(tool: str, args: dict) -> str:
    """模拟执行一个工具调用。真实系统这里会调用真正的 API/函数。"""
    if tool == "read_order":
        return f"[已执行] 查询订单 {args.get('order_id')}:配送中。"
    if tool == "send_email":
        return f"[已执行] 已向 {args.get('to')} 发送邮件。"
    if tool == "transfer_money":
        return f"[已执行] 已转账 {args.get('amount')} 元至 {args.get('to')}。"
    if tool == "delete_database":
        return "[已执行] 数据库已删除。"
    return f"[未知工具] {tool}"
