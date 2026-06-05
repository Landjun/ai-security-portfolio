"""
test_traditional.py —— 传统安全模块(01)单元测试。

验证每个案例的"不安全 vs 安全"行为差异:
- SQL 注入:不安全版被 admin' -- 绕过登录;安全版(参数化)不被绕过。
- XSS:不安全版输出可执行脚本;安全版转义为纯文本。
- 路径穿越:不安全版读到越界机密;安全版拦截 ../。
- 命令注入:安全版把含 && 的输入当作单个参数,不多执行命令。

用 importlib 按文件路径加载(目录名带连字符,不能直接 import)。
运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TRAD = os.path.join(_ROOT, "01-traditional-security")


def _load(rel_path, name):
    path = os.path.join(_TRAD, rel_path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestSQLInjection(unittest.TestCase):
    def setUp(self):
        self.m = _load(os.path.join("sql-injection", "demo.py"), "sqli_demo")

    def test_vulnerable_is_bypassed(self):
        conn = self.m.make_db()
        role = self.m.login_vulnerable(conn, "admin' --", "任意密码")
        self.assertEqual(role, "admin")          # 注入成功:无需密码登入 admin

    def test_secure_blocks_injection(self):
        conn = self.m.make_db()
        role = self.m.login_secure(conn, "admin' --", "任意密码")
        self.assertIsNone(role)                  # 参数化:注入失败

    def test_secure_normal_login_works(self):
        conn = self.m.make_db()
        self.assertEqual(self.m.login_secure(conn, "alice", "alice123"), "user")


class TestXSS(unittest.TestCase):
    def setUp(self):
        self.m = _load(os.path.join("xss", "demo.py"), "xss_demo")

    def test_vulnerable_keeps_script(self):
        out = self.m.render_vulnerable("<script>steal()</script>")
        self.assertIn("<script>", out)           # 未转义:脚本会执行

    def test_secure_escapes_script(self):
        out = self.m.render_secure("<script>steal()</script>")
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)     # 已转义为纯文本


class TestPathTraversal(unittest.TestCase):
    def setUp(self):
        self.m = _load(os.path.join("path-traversal", "demo.py"), "pt_demo")
        self.base, self.public = self.m.setup_lab()

    def test_vulnerable_reads_secret(self):
        content = self.m.read_vulnerable(self.public, os.path.join("..", "secret.txt"))
        self.assertIn("机密", content)            # 穿越成功

    def test_secure_blocks_traversal(self):
        with self.assertRaises(PermissionError):
            self.m.read_secure(self.public, os.path.join("..", "secret.txt"))

    def test_secure_allows_normal_file(self):
        self.assertIn("欢迎", self.m.read_secure(self.public, "welcome.txt"))


class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.m = _load(os.path.join("command-injection", "demo.py"), "ci_demo")

    def test_secure_treats_payload_as_single_arg(self):
        payload = "report.txt && echo INJECTED"
        out = self.m.run_secure(payload)
        # 整个 payload 作为单个文件名参数被打印,&& 未被解析、未多执行命令
        self.assertIn("report.txt && echo INJECTED", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
