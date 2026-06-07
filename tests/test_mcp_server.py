"""
test_mcp_server.py —— 码小安 MCP 服务器接入 CI(纯标准库,无重依赖)。

验证 MCP JSON-RPC 握手、工具发现,以及"只读放行 / 敏感无人确认默认拒绝"的审计关卡。
运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HELPER = os.path.join(_ROOT, "06-ai-development", "ai-coding-helper")


def _load_mcp():
    # 放到 sys.path 最前,并清掉可能被其它测试缓存的同名模块,确保加载到本目录版本
    sys.path.insert(0, _HELPER)
    for name in ("tools", "knowledge_base", "ch_mcp_server"):
        sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location("ch_mcp_server", os.path.join(_HELPER, "mcp_server.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mcp = _load_mcp()


class TestMCPServer(unittest.TestCase):
    def test_initialize_handshake(self):
        r = mcp.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(r["result"]["protocolVersion"], mcp.PROTOCOL_VERSION)

    def test_tools_list(self):
        r = mcp.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = {t["name"] for t in r["result"]["tools"]}
        self.assertTrue({"search_knowledge_base", "save_learning_note"} <= names)

    def test_readonly_tool_allowed(self):
        r = mcp.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                        "params": {"name": "search_knowledge_base", "arguments": {"keyword": "二分"}}})
        self.assertFalse(r["result"]["isError"])
        self.assertTrue(r["result"]["content"][0]["text"])

    def test_sensitive_tool_denied_headless(self):
        r = mcp.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                        "params": {"name": "save_learning_note", "arguments": {"content": "x"}}})
        self.assertTrue(r["result"]["isError"])  # 无人确认 -> 审计关卡拒绝

    def test_unknown_method_errors(self):
        r = mcp.handle({"jsonrpc": "2.0", "id": 5, "method": "no_such"})
        self.assertEqual(r["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
