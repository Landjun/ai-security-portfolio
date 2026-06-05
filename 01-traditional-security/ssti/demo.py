"""
demo.py —— 服务端模板注入(SSTI)本地演示:不安全 vs 安全。

原理:把用户输入当作模板"表达式"求值时(常见于误用模板引擎),攻击者可注入表达式
读取对象、配置,甚至命令执行。本演示用一个极简模板引擎说明原理,载荷无害。

运行:  python demo.py
"""

import html

# 一个"机密配置",用于演示 SSTI 能读到本不该暴露的数据
CONFIG = {"db_password": "DB-P@ss-9527"}


def render_vulnerable(template: str, name: str):
    """不安全:把 {{...}} 里的内容当 Python 表达式 eval(典型 SSTI 误用)。"""
    import re
    def repl(m):
        expr = m.group(1)
        return str(eval(expr, {"name": name, "CONFIG": CONFIG}))   # 危险:eval 用户可控表达式
    return re.sub(r"\{\{(.+?)\}\}", repl, template)


def render_secure(template: str, name: str):
    """安全:{{key}} 只做白名单变量替换 + HTML 转义,绝不 eval 表达式。"""
    import re
    allowed = {"name": name}
    def repl(m):
        key = m.group(1).strip()
        return html.escape(str(allowed.get(key, "")))   # 只查白名单,转义输出
    return re.sub(r"\{\{(.+?)\}\}", repl, template)


def line():
    print("-" * 64)


if __name__ == "__main__":
    print("=" * 64)
    print("SSTI 服务端模板注入演示")
    print("=" * 64)

    cases = [
        "你好 {{name}}",                  # 正常用法
        "计算:{{7*7}}",                   # 注入:表达式被求值
        "机密:{{CONFIG['db_password']}}",  # 注入:读到机密配置
    ]
    for t in cases:
        line()
        print(f"模板: {t}")
        print(f"  [不安全版] {render_vulnerable(t, '小明')}")
        print(f"  [安全版  ] {render_secure(t, '小明')}")

    line()
    print("\n结论:把用户输入当模板表达式 eval = 可读对象/配置,甚至命令执行;")
    print("只做白名单变量替换 + 输出转义,或用沙箱化模板引擎,不 eval 用户输入,是 SSTI 核心防御。")
