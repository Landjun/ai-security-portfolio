"""
tools.py —— 真实 Agent 可调用的工具(本地函数)+ function calling 的 schema。

function calling 的关键:大模型并不直接执行代码,它只是"决定"要调用哪个工具、
传什么参数;真正的执行由我们的 Python 代码完成,再把结果回填给模型。
所以工具的能力边界完全由我们掌控(这也是后续接入权限审计的基础)。
"""

import json

# —— 本地"数据库"(模拟)——
_ORDERS = {
    "A1001": {"status": "配送中", "amount": 199.0, "item": "蓝牙耳机"},
    "A1002": {"status": "已签收", "amount": 89.0, "item": "数据线"},
}

_POLICIES = {
    "退货": "支持 7 天无理由退货,商品需保持完好,退货运费由买家承担。",
    "发货": "付款后 48 小时内发货,节假日可能延迟。",
}


# —— 工具的真实实现 ——
def query_order(order_id: str) -> str:
    o = _ORDERS.get(order_id)
    if not o:
        return f"未找到订单 {order_id}。"
    return f"订单 {order_id}:商品「{o['item']}」,金额 {o['amount']} 元,状态:{o['status']}。"


def issue_refund(order_id: str, amount: float) -> str:
    # 敏感操作(此处为模拟)。真实场景应有权限校验——见模块 03 权限审计。
    o = _ORDERS.get(order_id)
    if not o:
        return f"退款失败:未找到订单 {order_id}。"
    return f"[模拟] 已为订单 {order_id} 发起退款 {amount} 元。"


def get_policy(topic: str) -> str:
    return _POLICIES.get(topic, f"暂无『{topic}』相关政策。")


# 名称 -> 函数 的分发表
TOOL_IMPL = {
    "query_order": query_order,
    "issue_refund": issue_refund,
    "get_policy": get_policy,
}


# —— 提供给大模型的工具描述(OpenAI/DeepSeek function calling 格式)——
TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "query_order",
        "description": "根据订单号查询订单的商品、金额和物流状态。",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "订单号,如 A1001"}},
            "required": ["order_id"],
        },
    }},
    {"type": "function", "function": {
        "name": "issue_refund",
        "description": "为指定订单发起退款(敏感操作)。",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "订单号"},
                "amount": {"type": "number", "description": "退款金额(元)"},
            },
            "required": ["order_id", "amount"],
        },
    }},
    {"type": "function", "function": {
        "name": "get_policy",
        "description": "查询某个主题的店铺政策,如『退货』『发货』。",
        "parameters": {
            "type": "object",
            "properties": {"topic": {"type": "string", "description": "政策主题,如 退货/发货"}},
            "required": ["topic"],
        },
    }},
]


def dispatch(name: str, arguments: str) -> str:
    """根据模型给出的工具名 + JSON 参数,执行对应的本地函数。"""
    fn = TOOL_IMPL.get(name)
    if fn is None:
        return f"未知工具:{name}"
    try:
        args = json.loads(arguments) if arguments else {}
    except json.JSONDecodeError:
        return f"参数解析失败:{arguments}"
    return fn(**args)
