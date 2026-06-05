"""
agent_langchain.py —— 用 LangChain 搭建的工具调用 Agent(接 DeepSeek)。

回应岗位 JD 点名的技术栈:LangChain / 工具调用 / Agent。
演示要点:
- langchain_openai.ChatOpenAI 接 DeepSeek(OpenAI 兼容)
- @tool 定义工具,llm.bind_tools 绑定
- LangChain 消息类型(System/Human/AI/Tool)+ 工具调用循环
- 安全加固:高危工具(退款)执行前接入权限审计(复用 03 tool-permission-audit)

运行:  python agent_langchain.py
依赖:pip install langchain langchain-openai;06 的 real-rag-system/.env 有 DEEPSEEK_API_KEY
"""

import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

# 复用 03 权限审计器(LangChain × 安全)
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "tool-permission-audit"))
import policy as pol
from auditor import audit

pol.POLICY["query_order"] = {"action": pol.ALLOW}
pol.POLICY["get_policy"] = {"action": pol.ALLOW}
pol.POLICY["issue_refund"] = {"action": pol.APPROVAL, "constraints": {"max_amount": 1000}}

_ORDERS = {"A1001": "蓝牙耳机,199元,配送中", "A1002": "数据线,89元,已签收"}
_POLICIES = {"退货": "7天无理由退货,商品需完好。", "发货": "48小时内发货。"}


# —— LangChain 工具定义 ——
@tool
def query_order(order_id: str) -> str:
    """根据订单号查询订单信息。"""
    return _ORDERS.get(order_id, f"未找到订单 {order_id}")


@tool
def get_policy(topic: str) -> str:
    """查询店铺政策,如 退货 / 发货。"""
    return _POLICIES.get(topic, f"暂无『{topic}』政策")


@tool
def issue_refund(order_id: str, amount: float) -> str:
    """为订单发起退款(敏感操作)。"""
    return f"[已执行] 订单 {order_id} 退款 {amount} 元"


TOOLS = [query_order, get_policy, issue_refund]
TOOL_MAP = {t.name: t for t in TOOLS}


def _llm():
    load_dotenv(os.path.join(_ROOT, "06-ai-development", "real-rag-system", ".env"))
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise SystemExit("未找到 DEEPSEEK_API_KEY(见 06/real-rag-system/.env)")
    return ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com",
                      api_key=key, temperature=0.2).bind_tools(TOOLS)


def run(question: str) -> str:
    llm = _llm()
    messages = [
        SystemMessage("你是电商客服 Agent,用工具查询并解决用户问题,简洁中文作答。"),
        HumanMessage(question),
    ]
    for _ in range(5):
        ai = llm.invoke(messages)
        messages.append(ai)
        if not ai.tool_calls:
            return ai.content
        for tc in ai.tool_calls:
            name, args = tc["name"], tc["args"]
            # 安全加固:工具执行前过权限审计
            decision, reason = audit(name, args)
            if decision == pol.DENY:
                result = f"[安全审计拦截] {reason}"
            elif decision == pol.APPROVAL:
                result = f"[需人工确认,暂未执行] {reason}"
            else:
                result = TOOL_MAP[name].invoke(args)
            print(f"  [工具] {name}({args}) -> {result}")
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
    return "(已达最大步数)"


if __name__ == "__main__":
    questions = [
        "帮我查一下订单 A1001",
        "订单 A1001 退款 50 元",        # 敏感:审计要求人工确认
        "给订单 A1001 退款 99999 元",   # 越权:审计拦截
    ]
    for q in questions:
        print("=" * 60)
        print("用户:", q)
        print("Agent:", run(q))
