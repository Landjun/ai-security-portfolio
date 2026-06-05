"""
vulnerable_agent.py —— 【故意有漏洞的 AI Agent · 代码审计靶场】

⚠️ 本文件**故意写得不安全**,仅用于代码审计教学。请勿在任何真实环境运行/部署。
每个工具函数都植入了一类典型漏洞,供 audit_scan.py 扫描、AUDIT-REPORT.md 分析。
"""

import os
import pickle
import sqlite3
import subprocess

import requests

# —— 漏洞0:硬编码机密(应放 .env / 密钥管理)——
SYSTEM_PROMPT = "你是企业助手,内部管理员密钥是 ADMIN-KEY-9527,不要告诉用户。"
API_KEY = "sk-deadbeefdeadbeefdeadbeefdeadbeef"


def run_code_tool(llm_output: str):
    """漏洞1:对大模型/用户输出直接 eval -> 任意代码执行。"""
    return eval(llm_output)                                   # 危险


def shell_tool(filename: str):
    """漏洞2:拼接命令 + shell=True -> 命令注入。"""
    cmd = f"cat {filename}"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def fetch_url_tool(url: str):
    """漏洞3:对用户提供的 URL 无白名单/无内网过滤 -> SSRF(可访问内网/元数据)。"""
    return requests.get(url, timeout=5).text                 # 危险


def read_file_tool(path: str):
    """漏洞4:直接拼接用户路径 -> 路径穿越(../ 越界读文件)。"""
    with open(os.path.join("data", path), encoding="utf-8") as f:
        return f.read()


def query_user_tool(user_id: str):
    """漏洞5:字符串拼接 SQL -> SQL 注入。"""
    conn = sqlite3.connect(":memory:")
    return conn.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchall()


def load_state_tool(blob: bytes):
    """漏洞6:对不可信数据 pickle 反序列化 -> 远程代码执行。"""
    return pickle.loads(blob)                                # 危险


def issue_refund_tool(amount: float):
    """漏洞7:高危资金动作无任何权限校验/上限 -> 过度授权(LLM06)。"""
    return f"[已执行] 退款 {amount} 元"
