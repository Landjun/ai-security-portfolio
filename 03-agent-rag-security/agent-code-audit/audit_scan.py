"""
audit_scan.py —— 半自动化代码审计扫描器(危险模式静态检测)。

对 Python 文件做基于规则的静态扫描,定位常见危险函数/反模式,辅助人工代码审计。
不是完整的污点分析,而是"快速定位审计入口"的实战小工具。

运行:  python audit_scan.py vulnerable_agent.py
       python audit_scan.py            # 默认扫描 vulnerable_agent.py
"""

import re
import sys

# 规则:(类别, 风险等级, 正则, 说明)
RULES = [
    ("代码执行", "高", r"\beval\s*\(", "eval() 执行字符串,若输入不可信=任意代码执行"),
    ("代码执行", "高", r"\bexec\s*\(", "exec() 执行字符串代码"),
    ("命令注入", "高", r"subprocess\.\w+\([^)]*shell\s*=\s*True", "shell=True 拼接命令=命令注入"),
    ("命令注入", "高", r"\bos\.system\s*\(", "os.system 执行 shell 命令"),
    ("反序列化", "高", r"pickle\.loads?\s*\(", "pickle 反序列化不可信数据=RCE"),
    ("反序列化", "高", r"yaml\.load\s*\((?![^)]*Loader)", "yaml.load 未指定安全 Loader"),
    ("SSRF", "高", r"requests\.\w+\(\s*[a-zA-Z_]\w*", "对变量 URL 发请求,缺白名单=SSRF"),
    ("SQL注入", "高", r"execute\(\s*f[\"']", "execute(f\"...\") 拼接 SQL=注入"),
    ("路径穿越", "中", r"open\(\s*os\.path\.join\([^,]+,\s*[a-zA-Z_]\w*", "用用户变量拼路径=路径穿越"),
    ("硬编码密钥", "高", r"sk-[A-Za-z0-9]{12,}", "硬编码 API Key"),
    ("硬编码密钥", "中", r"(密钥|password|passwd|secret|API_KEY)\s*=\s*[\"']", "硬编码凭证"),
]


def scan(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    findings = []
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            continue
        for cat, sev, pat, desc in RULES:
            if re.search(pat, line):
                findings.append((i, sev, cat, desc, line.strip()))
    return findings


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "vulnerable_agent.py"
    findings = scan(path)
    print("=" * 64)
    print(f"代码审计扫描:{path}")
    print("=" * 64)
    sev_count = {"高": 0, "中": 0, "低": 0}
    for ln, sev, cat, desc, code in findings:
        sev_count[sev] += 1
        print(f"\n[L{ln:>3}] ({sev}) {cat} —— {desc}")
        print(f"        {code}")
    print("\n" + "-" * 64)
    print(f"共发现 {len(findings)} 处可疑点(高 {sev_count['高']} / 中 {sev_count['中']} / 低 {sev_count['低']})")
    print("注:静态扫描用于定位审计入口,需结合人工确认数据流与可利用性(见 AUDIT-REPORT.md)。")


if __name__ == "__main__":
    main()
