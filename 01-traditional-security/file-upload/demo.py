"""
demo.py —— 文件上传漏洞本地演示:不安全 vs 安全。

原理:上传功能若只信任文件名/扩展名/Content-Type,攻击者可上传可执行脚本(webshell)
或用 ../ 穿越路径。本演示只做"是否接受 + 落地文件名"的判定,不真实写危险文件,完全无害。

运行:  python demo.py
"""

import os
import uuid

# 安全版:扩展名白名单 + 魔术字节(文件头)校验
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}
MAGIC = {b"\xff\xd8\xff": "jpg", b"\x89PNG": "png", b"GIF8": "gif", b"%PDF": "pdf"}


def save_vulnerable(filename, content: bytes):
    """不安全:直接用用户文件名落地(信任扩展名,允许穿越)。"""
    path = os.path.join("uploads", filename)
    return f"[落地] {os.path.normpath(path)}"


def ext_ok(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT


def magic_ok(content: bytes):
    return any(content.startswith(sig) for sig in MAGIC)


def save_secure(filename, content: bytes):
    """安全:扩展名白名单 + 文件头校验 + 随机文件名 + 固定目录。"""
    ext = os.path.splitext(filename)[1].lower()
    if not ext_ok(filename):
        return f"[拒绝] 扩展名 {ext or '(无)'} 不在白名单"
    if not magic_ok(content):
        return "[拒绝] 文件头与扩展名不符(疑似伪装)"
    safe_name = f"{uuid.uuid4().hex}{ext}"          # 随机名,丢弃用户原名
    return f"[落地] uploads/{safe_name}(原名 {filename} 已丢弃)"


def line():
    print("-" * 66)


if __name__ == "__main__":
    cases = [
        ("photo.jpg", b"\xff\xd8\xff\xe0JFIF..."),          # 正常图片(JPEG 文件头)
        ("shell.php", b"<?php system($_GET[c]); ?>"),       # webshell
        ("evil.jpg.php", b"<?php ... ?>"),                  # 双扩展名绕过
        ("../../var/www/x.php", b"<?php ... ?>"),           # 路径穿越
        ("fake.png", b"<?php ... ?>"),                      # 改扩展名伪装(文件头不符)
    ]
    print("=" * 66)
    print("文件上传漏洞演示")
    print("=" * 66)
    for fn, content in cases:
        line()
        print(f"上传文件名: {fn}")
        print(f"  [不安全版] {save_vulnerable(fn, content)}")
        print(f"  [安全版  ] {save_secure(fn, content)}")
    line()
    print("\n结论:信任用户文件名/扩展名 = 可上传 webshell 或穿越路径;")
    print("扩展名白名单 + 文件头校验 + 随机文件名 + 固定目录(+ 禁止该目录执行)是核心防御。")
