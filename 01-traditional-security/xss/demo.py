"""
demo.py —— 跨站脚本(XSS)本地演示:不安全 vs 安全 渲染对比。

原理:把用户输入未经转义地放进 HTML,浏览器会把其中的 <script> 当代码执行。
本演示只生成 HTML 字符串并对比,不启动浏览器,完全本地无害。

运行:  python demo.py
"""

import html


def render_vulnerable(comment: str) -> str:
    """不安全:用户输入直接拼进 HTML。"""
    return f"<div class='comment'>{comment}</div>"


def render_secure(comment: str) -> str:
    """安全:对输入做 HTML 转义后再渲染。"""
    return f"<div class='comment'>{html.escape(comment)}</div>"


def line():
    print("-" * 64)


if __name__ == "__main__":
    # 典型 XSS 载荷:窃取 cookie 的脚本(此处仅作字符串演示,不会执行)
    payload = "<script>steal(document.cookie)</script>"

    print("=" * 64)
    print("XSS 跨站脚本演示")
    print("=" * 64)
    print(f"用户提交的评论(恶意载荷): {payload}")

    line()
    print("[不安全版] 直接拼进 HTML:")
    out = render_vulnerable(payload)
    print(f"  生成的HTML: {out}")
    print("  -> 浏览器会把 <script> 当代码执行,cookie 被窃取!")

    line()
    print("[安全版] 先做 HTML 转义:")
    out = render_secure(payload)
    print(f"  生成的HTML: {out}")
    print("  -> <script> 变成纯文本显示,脚本不会执行。")

    line()
    print("\n结论:把用户输入当作 HTML 拼接 = 让输入变成可执行代码;")
    print("输出转义(+ CSP + HttpOnly Cookie)是 XSS 的核心防御。")
