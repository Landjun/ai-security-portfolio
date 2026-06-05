"""
secure_agent.py —— vulnerable_agent.py 的【安全修复版】。

逐项修复 AUDIT-REPORT.md 里的 7 类漏洞,体现"审计 → 修复 → 复测"的完整闭环。
对本文件再跑 audit_scan.py,高危发现应从 8 降到 0。
"""

import ast
import ipaddress
import json
import os
import sqlite3
import subprocess
import urllib.parse

# 修复 V0:机密走环境变量,系统提示词不含机密
SYSTEM_PROMPT = "你是企业助手,请勿泄露任何内部信息。"
API_KEY = os.environ.get("AGENT_API_KEY", "")          # 从环境读取,不硬编码

_DATA_DIR = os.path.realpath("data")
_URL_ALLOW = {"api.example.com", "data.example.com"}


def run_code_tool(expr: str):
    """修复 V1:不用 eval;只用 ast.literal_eval 解析字面量,不执行任意代码。"""
    try:
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        return "[拒绝] 仅支持安全的字面量解析"


def shell_tool(filename: str):
    """修复 V2:参数列表 + shell=False,文件名做白名单。"""
    if not filename.isalnum():
        return "[拒绝] 文件名非法"
    return subprocess.run(["cat", filename], shell=False,
                          capture_output=True, text=True).stdout


def _url_safe(url: str):
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https"):
        return False
    host = (p.hostname or "").lower()
    if host not in _URL_ALLOW:
        return False
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False
    except ValueError:
        pass
    return True


def fetch_url_tool(url: str):
    """修复 V3:URL 白名单 + 拒绝内网/保留地址(此处模拟获取)。"""
    if not _url_safe(url):
        return "[拒绝] URL 不在白名单或指向内网"
    return f"[模拟] 已安全获取 {url}"


def _safe_path(name: str):
    full = os.path.realpath(os.path.join(_DATA_DIR, name))
    if full == _DATA_DIR or full.startswith(_DATA_DIR + os.sep):
        return full
    return None


def read_file_tool(name: str):
    """修复 V4:realpath 规范化 + 根目录边界校验。"""
    full = _safe_path(name)
    if full is None:
        return "[拒绝] 路径越界"
    if not os.path.exists(full):
        return "[未找到]"
    with open(full, encoding="utf-8") as f:
        return f.read()


def query_user_tool(user_id: str):
    """修复 V5:参数化查询。"""
    conn = sqlite3.connect(":memory:")
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()


def load_state_tool(text: str):
    """修复 V6:用 json 只还原数据,不执行代码。"""
    return json.loads(text)


def issue_refund_tool(amount: float, approved: bool = False):
    """修复 V7:金额上限 + 人工确认(approved)才执行。"""
    if amount > 1000:
        return "[拒绝] 超过单笔上限 1000,需走人工审批"
    if not approved:
        return "[挂起] 退款需人工确认后执行"
    return f"[已执行] 退款 {amount} 元"
