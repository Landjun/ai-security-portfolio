"""
gateway.py —— LLM 安全网关:把所有检测器封装成统一拦截中间件。

三道关卡(任何 LLM 应用都可按需接入):
  1. check_input(text)        输入护栏:提示注入 + 越狱检测
  2. check_action(tool, args) 动作审计:工具调用最小权限
  3. check_output(text)       输出扫描:机密/系统提示词泄露

设计理念:安全能力应是"可插拔的统一中间件",而不是散落各处的一次性脚本。
每次检查都写入审计日志,便于追溯。

复用:
- 注入检测器  03 rag-injection-detector/detector.py  scan_text
- 越狱检测器  02 jailbreak/defense.py                detect
- 权限审计器  03 tool-permission-audit/auditor.py    audit
"""

import os
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "rag-injection-detector"))
sys.path.insert(0, os.path.join(_ROOT, "02-ai-security", "jailbreak"))
sys.path.insert(0, os.path.join(_ROOT, "03-agent-rag-security", "tool-permission-audit"))

from detector import scan_text            # 注入检测
from defense import detect as jb_detect   # 越狱检测
import policy as pol                       # 权限策略
from auditor import audit                  # 权限审计

# 输出泄露特征:机密字符串 / 系统提示词外泄迹象
OUTPUT_LEAK_PATTERNS = {
    "API密钥": r"sk-[A-Za-z0-9]{12,}",
    "演示机密": r"(ADMIN-KEY-\w+|SK-DEMO-\w+|FREE-VIP-\w+)",
    "密钥泄露措辞": r"(密钥|密码|口令)\s*(是|为|:|：)\s*\S+",
    "系统提示词外泄": r"(系统提示词|system prompt)\s*(是|为|:|：)",
}


class Decision:
    """统一决策结果。status ∈ {allow, review, deny, block}。"""
    def __init__(self, layer, status, reasons=None):
        self.layer = layer
        self.status = status
        self.allowed = (status == "allow")
        self.reasons = reasons or []

    def __str__(self):
        tag = {"allow": "放行", "review": "需人工确认",
               "deny": "拒绝", "block": "拦截"}[self.status]
        extra = f" | {'; '.join(self.reasons)}" if self.reasons else ""
        return f"[{self.layer}] {tag}{extra}"


class SecurityGateway:
    def __init__(self):
        self.log = []

    def _record(self, decision, target):
        self.log.append({
            "ts": time.strftime("%H:%M:%S"), "layer": decision.layer,
            "status": decision.status, "target": target, "reasons": decision.reasons,
        })

    # 1) 输入护栏
    def check_input(self, text: str) -> Decision:
        reasons = []
        inj, inj_cats = scan_text(text)
        jb, jb_cats = jb_detect(text)
        if inj:
            reasons.append("提示注入:" + ",".join(inj_cats))
        if jb:
            reasons.append("越狱:" + ",".join(jb_cats))
        d = Decision("输入护栏", "block" if reasons else "allow", reasons)
        self._record(d, text)
        return d

    # 2) 动作审计
    def check_action(self, tool: str, args: dict) -> Decision:
        decision, reason = audit(tool, args or {})
        status = {pol.ALLOW: "allow", pol.APPROVAL: "review", pol.DENY: "deny"}[decision]
        d = Decision("动作审计", status, [reason] if status != "allow" else [])
        self._record(d, f"{tool}({args})")
        return d

    # 3) 输出扫描
    def check_output(self, text: str) -> Decision:
        reasons = []
        for name, pat in OUTPUT_LEAK_PATTERNS.items():
            if re.search(pat, text or "", flags=re.IGNORECASE):
                reasons.append(name)
        d = Decision("输出扫描", "block" if reasons else "allow", reasons)
        self._record(d, text)
        return d

    def dump_log(self):
        print("\n--- 网关审计日志 ---")
        for e in self.log:
            print(f"  {e['ts']} [{e['layer']}] {e['status']:6} <- {str(e['target'])[:40]}")
