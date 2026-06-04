"""
demo.py —— 路径穿越(Path Traversal)本地演示:不安全 vs 安全 对比。

原理:应用用用户输入拼接文件路径时,攻击者用 ../ 跳出预期目录,读取任意文件
(如 /etc/passwd、配置、密钥)。本演示在本地临时目录构造靶场,完全无害。

运行:  python demo.py
"""

import os
import tempfile


def setup_lab():
    """构造靶场:一个公开目录(放正常文件)+ 一个'机密'文件在其外层。"""
    base = tempfile.mkdtemp(prefix="ptlab_")
    public = os.path.join(base, "public")
    os.makedirs(public, exist_ok=True)
    with open(os.path.join(public, "welcome.txt"), "w", encoding="utf-8") as f:
        f.write("欢迎访问公开文件。")
    # 机密文件放在 public 的外层(正常情况下不应被访问到)
    with open(os.path.join(base, "secret.txt"), "w", encoding="utf-8") as f:
        f.write("机密:数据库密码=DB-P@ss-9527")
    return base, public


def read_vulnerable(public_dir, user_path):
    """不安全:直接把用户输入拼到公开目录后面。"""
    full = os.path.join(public_dir, user_path)
    print(f"    解析到的真实路径: {os.path.normpath(full)}")
    with open(full, encoding="utf-8") as f:
        return f.read()


def read_secure(public_dir, user_path):
    """安全:规范化后校验最终路径仍在公开目录内,否则拒绝。"""
    base = os.path.realpath(public_dir)
    full = os.path.realpath(os.path.join(base, user_path))
    if not (full == base or full.startswith(base + os.sep)):
        raise PermissionError("拒绝:试图访问公开目录之外的文件")
    with open(full, encoding="utf-8") as f:
        return f.read()


def line():
    print("-" * 64)


if __name__ == "__main__":
    base, public = setup_lab()
    # 穿越载荷:用 ../ 跳出 public 去读外层的 secret.txt
    payload = os.path.join("..", "secret.txt")

    print("=" * 64)
    print("路径穿越演示")
    print("=" * 64)
    print(f"公开目录: {public}")
    print(f"攻击者请求的文件名: {payload}")

    line()
    print("[不安全版] 直接拼接路径:")
    try:
        print("  读到内容:", read_vulnerable(public, payload))
        print("  -> 穿越成功!读到了公开目录之外的机密文件")
    except Exception as e:
        print("  异常:", e)

    line()
    print("[安全版] 规范化 + 边界校验:")
    try:
        print("  读到内容:", read_secure(public, payload))
    except Exception as e:
        print(f"  {e}   <- 穿越被拦截")

    line()
    print("\n正常访问(welcome.txt)在安全版下仍可读:")
    print("  ", read_secure(public, "welcome.txt"))

    line()
    print("\n结论:拼接用户路径 = 允许 ../ 跳出目录;")
    print("规范化路径后校验它仍在允许的根目录内,是路径穿越的核心防御。")
