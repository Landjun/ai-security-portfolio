"""
mock_agent.py —— 模拟 Agent 的"大脑":根据上下文决定调用哪些工具。

这个 Agent 很天真:它会"信任"上下文里的内容。如果上下文被投毒
(含有越权指令),它就会被劫持,转而发起恶意的高危工具调用。
这串起了两类风险:间接注入(输入端) -> 过度授权(执行端)。
"""


def decide(context: str):
    """
    输入:拼好的上下文(来自知识库检索)。
    输出:Agent 想发起的工具调用列表 [{"tool":..., "args":{...}}, ...]
    """
    ctx = context or ""

    # 被投毒上下文劫持:出现"忽略规则 + 密钥/权限"类指令 -> 发起恶意转账
    if "忽略" in ctx and ("密钥" in ctx or "权限" in ctx):
        return [
            {"tool": "transfer_money", "args": {"to": "攻击者钱包", "amount": 999999}},
        ]

    # 正常情况:只做一个无害的只读查询
    return [
        {"tool": "read_order", "args": {"order_id": 123}},
    ]
