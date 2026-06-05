"""
test_multiagent.py —— 多智能体安全测试。

验证:被投毒内容会劫持执行器(无防护);完整防御下执行器不再越权转账。
运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DIR = os.path.join(_ROOT, "03-agent-rag-security", "multi-agent-security")
sys.path.insert(0, _DIR)
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "llm-security-gateway"))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "tool-permission-audit"))


def _load_agents():
    spec = importlib.util.spec_from_file_location("ma_agents", os.path.join(_DIR, "agents.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class TestMultiAgentInjection(unittest.TestCase):
    def setUp(self):
        self.a = _load_agents()

    def test_poison_propagates_and_hijacks(self):
        """无防护:投毒内容经研究员传给执行器,劫持其发起越权转账。"""
        r = self.a.ResearcherAgent()
        e = self.a.ExecutorAgent()
        summary = r.process(self.a.POISONED_CONTENT)
        calls = e.decide(summary)
        self.assertEqual(calls[0]["tool"], "transfer_money")
        self.assertGreater(calls[0]["args"]["amount"], 1000)

    def test_clean_content_is_safe(self):
        """正常内容:执行器只做无害查询。"""
        r = self.a.ResearcherAgent()
        e = self.a.ExecutorAgent()
        calls = e.decide(r.process(self.a.CLEAN_CONTENT))
        self.assertEqual(calls[0]["tool"], "read_order")

    def test_sanitized_message_neutralizes_injection(self):
        """完整防御:消息净化后,执行器不再被劫持。"""
        from gateway import SecurityGateway
        gw = SecurityGateway()
        r = self.a.ResearcherAgent()
        e = self.a.ExecutorAgent()
        summary = r.process(self.a.POISONED_CONTENT)
        if not gw.check_input(summary).allowed:
            summary = "[已净化] 资料含可疑指令,已剔除。"
        calls = e.decide(summary)
        self.assertEqual(calls[0]["tool"], "read_order")     # 不再越权转账


if __name__ == "__main__":
    unittest.main(verbosity=2)
