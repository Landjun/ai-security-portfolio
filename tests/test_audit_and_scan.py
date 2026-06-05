"""
test_audit_and_scan.py —— 代码审计修复闭环 + 自动化评测扫描器 测试。

- 漏洞版静态扫描有发现、安全版 0 发现(验证修复闭环)。
- 自动化评测扫描器对所有用例判定正确(安全得分满分)。

运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_AUDIT = os.path.join(_ROOT, "03-agent-rag-security", "agent-code-audit")
_ASSESS = os.path.join(_ROOT, "03-agent-rag-security", "ai-security-assessment")
sys.path.insert(0, _AUDIT)
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "llm-security-gateway"))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class TestCodeAuditFixLoop(unittest.TestCase):
    def setUp(self):
        self.scan = _load(os.path.join(_AUDIT, "audit_scan.py"), "audit_scan_mod").scan

    def test_vulnerable_has_findings(self):
        n = len(self.scan(os.path.join(_AUDIT, "vulnerable_agent.py")))
        self.assertGreaterEqual(n, 6, "漏洞版应有多处发现")

    def test_secure_has_no_findings(self):
        n = len(self.scan(os.path.join(_AUDIT, "secure_agent.py")))
        self.assertEqual(n, 0, "安全版应 0 发现(修复闭环)")


class TestAssessmentScanner(unittest.TestCase):
    def test_scanner_full_score(self):
        scanner = _load(os.path.join(_ASSESS, "scanner.py"), "scanner_mod")
        rows = scanner.run()
        passed, total = scanner.score(rows)
        self.assertEqual(passed, total, "评测扫描器应全部通过")
        self.assertGreaterEqual(total, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
