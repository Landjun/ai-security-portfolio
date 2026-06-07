"""
audit_scanner.py —— 智能合约静态审计扫描器(纯静态、不编译、不执行、不上链)。

定位:像 03 的 agent-code-audit 扫描器一样,做"快速定位危险模式"的第一道关,
再交人工/AI 语义复核(见各漏洞目录 README)。基于正则与轻量函数块分析,
覆盖语法上可检测的漏洞类别;重入用"外部调用是否在状态更新之前"的函数级启发式。

诚实声明:静态启发式存在误报/漏报。重入、预言机操纵、抢跑等需结合数据流与链上语义复核;
本工具用于"缩小排查范围",不替代人工审计。

用法:
    python audit_scanner.py            # 扫描本目录所有 .sol
    python audit_scanner.py <路径>      # 扫描指定文件或目录
"""

import os
import re
import sys

SEV = {"HIGH": "高危", "MED": "中危", "LOW": "低危", "INFO": "提示"}

# 链上可预测变量 + 随机上下文(keccak256/取模),才判为弱随机,避免误伤"时间锁/新鲜度校验"
_BLOCK_VAR = re.compile(r"block\.(timestamp|prevrandao|number)\b|blockhash\s*\(")
_RANDOM_CTX = re.compile(r"keccak256|%")

# 行级正则规则:(id, 严重度, 正则, 说明)
LINE_RULES = [
    ("ACCESS-TXORIGIN", "HIGH", re.compile(r"tx\.origin"),
     "用 tx.origin 鉴权,可被钓鱼中转绕过 -> 改用 msg.sender"),
    ("DELEGATECALL", "HIGH", re.compile(r"\bdelegatecall\b"),
     "delegatecall:确认目标地址受控、代理/实现存储布局对齐"),
    ("ORACLE-SPOT", "HIGH", re.compile(r"getReserves\s*\("),
     "用 DEX 现货储备定价,可被闪电贷操纵 -> 用 TWAP / 去中心化预言机"),
    ("ARITH-UNCHECKED", "MED", re.compile(r"\bunchecked\b"),
     "unchecked 块:确认其中无未校验边界的资金算术(下溢/溢出)"),
]


def _scan_lines(path, lines):
    findings = []
    for i, raw in enumerate(lines, 1):
        line = raw.split("//", 1)[0]  # 去掉行内注释,减少对注释里关键词的误报
        for vid, sev, pat, msg in LINE_RULES:
            if pat.search(line):
                findings.append((path, i, vid, sev, msg))
        # 弱随机:仅当链上变量与随机上下文(keccak256/取模)同现才告警
        if _BLOCK_VAR.search(line) and _RANDOM_CTX.search(line):
            findings.append((path, i, "BAD-RANDOM", "HIGH",
                             "链上变量作随机源,可被预测/操纵 -> 用 Chainlink VRF 或 commit-reveal"))
        # 未检查的低级调用:.send( 一律提示;.call{value 未用 (bool 接收返回值时提示
        if re.search(r"\.send\s*\(", line):
            findings.append((path, i, "UNCHECKED-CALL", "MED",
                             ".send 返回值未校验 -> 检查返回值或用 call+require"))
        elif re.search(r"\.call\{value", line) and "(bool" not in line and "require" not in line:
            findings.append((path, i, "UNCHECKED-CALL", "MED",
                             "低级 call 返回值疑似未校验 -> (bool ok,)=...; require(ok)"))
    return findings


def _scan_dos(path, lines):
    """for 循环内对外部地址转账(push 模式):单点失败/gas 耗尽 DoS。"""
    findings = []
    for i, raw in enumerate(lines):
        if re.search(r"\bfor\s*\(", raw):
            for j in range(i, min(i + 12, len(lines))):
                if re.search(r"\bfunction\b", lines[j]) and j > i:
                    break
                if re.search(r"\.(transfer|send)\s*\(|\.call\{value", lines[j]):
                    findings.append((path, i + 1, "DOS-PUSH", "MED",
                                     "for 循环内对外部地址转账(push 模式)-> 改拉模式 pull payment"))
                    break
    return findings


def _functions(lines):
    """把源码粗分成函数块:返回 [(header_line_idx, header_text, [(lineno, text), ...])]。"""
    funcs = []
    n = len(lines)
    i = 0
    while i < n:
        if re.search(r"\bfunction\b", lines[i]):
            depth = 0
            started = False
            body = []
            j = i
            while j < n:
                depth += lines[j].count("{") - lines[j].count("}")
                body.append((j + 1, lines[j]))
                if "{" in lines[j]:
                    started = True
                if started and depth <= 0:
                    break
                j += 1
            funcs.append((i, lines[i], body))
            i = j + 1
        else:
            i += 1
    return funcs


_STATE_WRITE = re.compile(r"\w+\s*\[[^\]]*\]\s*[-+]?=[^=]|^\s*\w+\s*=\s*[^=]")
_TYPE_DECL = re.compile(r"\b(bool|uint\d*|int\d*|address|bytes\d*|string|mapping)\b")
_EXT_CALL = re.compile(r"\.call\{value|\.send\s*\(|\.transfer\s*\(")


def _scan_reentrancy(path, lines):
    """函数级启发式:外部转账调用之后还有状态写入,且无 nonReentrant -> 疑似重入(CEI 违背)。"""
    findings = []
    for _, header, body in _functions(lines):
        if "nonReentrant" in header:
            continue
        call_k = None
        for k, (_, txt) in enumerate(body):
            if _EXT_CALL.search(txt.split("//", 1)[0]):
                call_k = k
                call_line = body[k][0]
                break
        if call_k is None:
            continue
        for (_, txt) in body[call_k + 1:]:
            code = txt.split("//", 1)[0]
            if _STATE_WRITE.search(code) and not _TYPE_DECL.search(code):
                findings.append((path, call_line, "REENTRANCY", "HIGH",
                                 "外部调用在状态更新之前(CEI 违背)且无重入锁 -> CEI + nonReentrant"))
                break
    return findings


def _scan_sig_replay(path, lines):
    """文件级:用了 ecrecover 但全文件无 nonce -> 疑似签名重放(无防重放)。"""
    text = "\n".join(l.split("//", 1)[0] for l in lines)
    if "ecrecover" in text and "nonce" not in text:
        for i, l in enumerate(lines, 1):
            if "ecrecover" in l.split("//", 1)[0]:
                return [(path, i, "SIG-REPLAY", "HIGH",
                         "ecrecover 无 nonce/防重放 -> 加 nonce + 绑定合约地址/chainid(EIP-712)")]
    return []


def _scan_selfdestruct(path, lines):
    """函数级:selfdestruct 所在函数无访问控制 -> 无保护自毁(SWC-106)。"""
    findings = []
    for _, header, body in _functions(lines):
        guarded = "onlyOwner" in header or any(
            "require(msg.sender" in txt.replace(" ", "") for _, txt in body)
        sd_line = None
        for ln, txt in body:
            if "selfdestruct(" in txt.split("//", 1)[0]:
                sd_line = ln
                break
        if sd_line and not guarded:
            findings.append((path, sd_line, "SELFDESTRUCT", "HIGH",
                             "无访问控制的 selfdestruct -> 加 onlyOwner,或改可暂停+有序撤回"))
    return findings


def scan_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = []
    out += _scan_lines(path, lines)
    out += _scan_dos(path, lines)
    out += _scan_reentrancy(path, lines)
    out += _scan_sig_replay(path, lines)
    out += _scan_selfdestruct(path, lines)
    return out


def scan_path(target):
    sol_files = []
    if os.path.isfile(target) and target.endswith(".sol"):
        sol_files = [target]
    else:
        for root, _, files in os.walk(target):
            for fn in files:
                if fn.endswith(".sol"):
                    sol_files.append(os.path.join(root, fn))
    findings = []
    for p in sorted(sol_files):
        findings += scan_file(p)
    return findings, sol_files


def _report(findings, sol_files):
    print(f"扫描 {len(sol_files)} 个 .sol 文件,命中 {len(findings)} 处疑似风险(静态启发式,需人工复核):\n")
    by_file = {}
    for path, line, vid, sev, msg in findings:
        by_file.setdefault(path, []).append((line, vid, sev, msg))
    for path in sorted(by_file):
        rel = os.path.relpath(path)
        print(f"== {rel} ==")
        for line, vid, sev, msg in sorted(by_file[path]):
            print(f"  L{line:<3} [{SEV.get(sev, sev)}] {vid}: {msg}")
        print()


def _self_test():
    """离线自测:每个 Vulnerable.sol 命中其签名类别;Vulnerable 总命中 > Fixed 总命中。"""
    here = os.path.dirname(os.path.abspath(__file__))
    expect = {
        "reentrancy/Vulnerable.sol": "REENTRANCY",
        "arithmetic-overflow/Vulnerable.sol": "ARITH-UNCHECKED",
        "access-control/Vulnerable.sol": "ACCESS-TXORIGIN",
        "unchecked-call/Vulnerable.sol": "UNCHECKED-CALL",
        "oracle-manipulation/Vulnerable.sol": "ORACLE-SPOT",
        "denial-of-service/Vulnerable.sol": "DOS-PUSH",
        "bad-randomness/Vulnerable.sol": "BAD-RANDOM",
        "delegatecall/Vulnerable.sol": "DELEGATECALL",
        "signature-replay/Vulnerable.sol": "SIG-REPLAY",
        "unprotected-selfdestruct/Vulnerable.sol": "SELFDESTRUCT",
    }
    ok = 0
    for rel, vid in expect.items():
        fs = scan_file(os.path.join(here, *rel.split("/")))
        hit = any(f[2] == vid for f in fs)
        print(f"[{'OK' if hit else 'NG'}] {rel} -> 期望命中 {vid}:{'是' if hit else '否'}")
        ok += hit
    vuln_total = sum(len(scan_file(os.path.join(here, *r.split("/"))))
                     for r in expect)
    fixed_total = sum(len(scan_file(os.path.join(here, *r.replace("Vulnerable", "Fixed").split("/"))))
                      for r in expect)
    print(f"\n签名命中:{ok}/{len(expect)};Vulnerable 总命中 {vuln_total} > Fixed 总命中 {fixed_total}:"
          f"{'是' if vuln_total > fixed_total else '否'}")
    assert ok == len(expect) and vuln_total > fixed_total, "扫描器自测未通过"
    print("audit_scanner 自测通过。")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _self_test()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
        f, files = scan_path(target)
        _report(f, files)
