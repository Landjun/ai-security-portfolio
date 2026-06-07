"""
mcp_server.py —— 把「码小安」的工具暴露成 MCP 服务器(B7 补强)。

MCP(Model Context Protocol)是 Anthropic 推的"AI 应用 ↔ 工具/数据"标准协议:
JSON-RPC 2.0 over stdio。任何 MCP 客户端(Claude Desktop / IDE 插件等)都能发现并调用本服务暴露的工具。

本实现用**纯标准库**手写最小 MCP 服务端(initialize / tools/list / tools/call),
复用 tools.py 的工具定义与**权限审计关卡**——安全亮点:服务器无人值守,
敏感动作(写笔记)在"无人确认"时默认拒绝,只读工具放行,体现"MCP 暴露工具也要管权限"。

(与 03 mcp-security 的"攻防视角"互补:那边研究 MCP 风险,这边证明会用 MCP 落地。)

用法:
    python mcp_server.py             # 作为 MCP 服务器,从 stdin 读 JSON-RPC,stdout 回响应
    python mcp_server.py --selftest  # 离线自测协议握手与工具调用(无需 key)
"""

import json
import sys

from tools import TOOL_SCHEMAS, dispatch

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "coding-helper-mcp", "version": "0.1.0"}


def _ok(rid, result):
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _err(rid, code, message):
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}}


def handle(req: dict):
    """处理一条 JSON-RPC 请求,返回响应 dict;通知类(无 id)返回 None。"""
    method = req.get("method")
    rid = req.get("id")
    params = req.get("params") or {}

    if method == "initialize":
        return _ok(rid, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })

    if method in ("notifications/initialized", "initialized"):
        return None  # 通知,无需响应

    if method == "ping":
        return _ok(rid, {})

    if method == "tools/list":
        tools = [{
            "name": t["function"]["name"],
            "description": t["function"]["description"],
            "inputSchema": t["function"]["parameters"],
        } for t in TOOL_SCHEMAS]
        return _ok(rid, {"tools": tools})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        # 无人值守:敏感动作(APPROVAL)在无确认时默认拒绝;只读工具放行(审计关卡)
        text = dispatch(name, args, confirm=lambda *a: False)
        is_error = text.startswith(("[审计拒绝]", "[已取消]", "[错误]"))
        return _ok(rid, {"content": [{"type": "text", "text": text}], "isError": is_error})

    return _err(rid, -32601, f"method not found: {method}")


def serve():
    """MCP stdio 主循环:逐行读 JSON-RPC,写回响应。"""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def _self_test():
    """离线自测:协议握手 + 工具发现 + 工具调用(含审计关卡)。"""
    init = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert init["result"]["protocolVersion"] == PROTOCOL_VERSION, init

    lst = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    names = {t["name"] for t in lst["result"]["tools"]}
    assert {"search_knowledge_base", "save_learning_note"} <= names, names

    # 只读工具:放行,返回内容
    call = handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                   "params": {"name": "search_knowledge_base", "arguments": {"keyword": "二分"}}})
    assert call["result"]["isError"] is False and call["result"]["content"][0]["text"], call

    # 敏感写工具:无人确认 -> 审计关卡默认拒绝
    sens = handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                   "params": {"name": "save_learning_note", "arguments": {"content": "x"}}})
    assert sens["result"]["isError"] is True and "已取消" in sens["result"]["content"][0]["text"], sens

    # 未知方法 -> JSON-RPC 错误
    bad = handle({"jsonrpc": "2.0", "id": 5, "method": "no_such"})
    assert bad["error"]["code"] == -32601, bad

    print("mcp_server 自测通过:握手 / 工具发现 / 只读放行 / 敏感默认拒绝 / 未知方法报错 均正确")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _self_test()
    else:
        serve()
