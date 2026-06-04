"""
demo.py —— 命令注入本地演示:不安全 vs 安全 对比(无害载荷)。

原理:把用户输入拼进 shell 命令并交给 shell 执行,攻击者可用 ; && | 等
追加额外命令。本演示用无害载荷(追加一个 echo)说明原理,不执行任何危险命令。

运行:  python demo.py
"""

import subprocess
import sys


def run_vulnerable(filename: str):
    """不安全:拼接成字符串 + shell=True,shell 会解析 ; && 等。"""
    cmd = f"echo 正在处理文件: {filename}"
    print(f"    将交给 shell 执行: {cmd}")
    # 演示用:真实危害在于 filename 含 '; 额外命令'。此处用无害 echo 体现"多执行了一条"。
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def run_secure(filename: str):
    """安全:参数以列表传入 + 不经过 shell(shell=False),输入只当一个参数。
    用 Python 解释器充当'处理文件的命令'(跨平台稳定),关键在于 filename 作为单个 argv 传入。"""
    code = "import sys; print('正在处理文件:', sys.argv[1])"
    args = [sys.executable, "-c", code, filename]
    return subprocess.run(args, shell=False, capture_output=True, text=True).stdout.strip()


def line():
    print("-" * 64)


if __name__ == "__main__":
    # 无害注入载荷:正常文件名后追加一条 echo,模拟"被多执行了一条命令"
    payload = 'report.txt && echo [攻击者注入的额外命令被执行了]'

    print("=" * 64)
    print("命令注入演示(无害载荷)")
    print("=" * 64)
    print(f"用户输入的文件名: {payload}")

    line()
    print("[不安全版] 字符串拼接 + shell=True:")
    out = run_vulnerable(payload)
    print("  输出:")
    for ln in out.splitlines():
        print("   ", ln)
    print("  -> 注意:&& 后面那条命令也被执行了(真实场景里可能是 rm/下载木马)")

    line()
    print("[安全版] 参数列表 + shell=False:")
    out = run_secure(payload)
    print(f"  输出: {out}")
    print("  -> 整个输入被当作一个文件名参数,&& 不被解析,不会多执行命令。")

    line()
    print("\n结论:拼接命令交给 shell = 让输入能控制命令结构;")
    print("用参数列表 + shell=False(或严格白名单/转义)从根本上避免命令注入。")
