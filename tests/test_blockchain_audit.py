"""
test_blockchain_audit.py —— 区块链智能合约静态审计扫描器测试(接入 CI)。

验证 08-blockchain-security 的 audit_scanner:
- 每个 Vulnerable.sol 命中其签名漏洞类别(11 类靶场,10 类可静态定位)。
- 漏洞版总命中数 > 修复版(证明修复确实消除了危险模式)。
- 修复版的重入/签名重放/自毁不再被对应规则命中(关键修复生效)。

运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BC = os.path.join(_ROOT, "08-blockchain-security")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


scanner = _load(os.path.join(_BC, "audit_scanner.py"), "bc_audit_scanner")

# 每个漏洞主题 -> 期望被命中的签名类别(front-running 需语义复核,不在静态签名内)
EXPECT = {
    "reentrancy": "REENTRANCY",
    "arithmetic-overflow": "ARITH-UNCHECKED",
    "access-control": "ACCESS-TXORIGIN",
    "unchecked-call": "UNCHECKED-CALL",
    "oracle-manipulation": "ORACLE-SPOT",
    "denial-of-service": "DOS-PUSH",
    "bad-randomness": "BAD-RANDOM",
    "delegatecall": "DELEGATECALL",
    "signature-replay": "SIG-REPLAY",
    "unprotected-selfdestruct": "SELFDESTRUCT",
}


def _ids(path):
    return {f[2] for f in scanner.scan_file(path)}


class TestBlockchainAuditScanner(unittest.TestCase):
    def test_each_vulnerable_hits_signature(self):
        for topic, vid in EXPECT.items():
            path = os.path.join(_BC, topic, "Vulnerable.sol")
            self.assertIn(vid, _ids(path), f"{topic}/Vulnerable.sol 应命中 {vid}")

    def test_vulnerable_more_findings_than_fixed(self):
        vuln = sum(len(scanner.scan_file(os.path.join(_BC, t, "Vulnerable.sol"))) for t in EXPECT)
        fixed = sum(len(scanner.scan_file(os.path.join(_BC, t, "Fixed.sol"))) for t in EXPECT)
        self.assertGreater(vuln, fixed, "漏洞版总命中应多于修复版")

    def test_key_fixes_clear_their_signature(self):
        # 关键修复:重入加 CEI+锁、签名加 nonce、自毁加 onlyOwner -> 对应签名应消失
        for topic, vid in [("reentrancy", "REENTRANCY"),
                           ("signature-replay", "SIG-REPLAY"),
                           ("unprotected-selfdestruct", "SELFDESTRUCT")]:
            path = os.path.join(_BC, topic, "Fixed.sol")
            self.assertNotIn(vid, _ids(path), f"{topic}/Fixed.sol 不应再命中 {vid}")


if __name__ == "__main__":
    unittest.main()
