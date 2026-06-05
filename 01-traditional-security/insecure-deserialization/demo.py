"""
demo.py —— 不安全反序列化本地演示:pickle 危险 vs json 安全。

原理:pickle 反序列化会执行对象的 __reduce__,对不可信数据 pickle.loads 即可被
远程代码执行(RCE)。本演示用**无害载荷**(只打印一句话)说明"反序列化会执行代码",
不做任何真实危害。运行:  python demo.py
"""

import json
import pickle


class HarmlessPayload:
    """模拟恶意对象:反序列化时会执行 __reduce__ 返回的调用。
    这里只让它 print 一句话(无害),真实攻击这里可能是 os.system(...)。"""
    def __reduce__(self):
        return (print, ("[反序列化执行] 我本可以是 os.system('rm -rf /') —— 这就是 RCE",))


def load_vulnerable(blob: bytes):
    """不安全:对不可信字节直接 pickle.loads。"""
    return pickle.loads(blob)                       # 危险:会执行 __reduce__


def load_secure(text: str):
    """安全:用 json 解析,只还原数据,绝不执行代码。"""
    return json.loads(text)


def line():
    print("-" * 64)


if __name__ == "__main__":
    print("=" * 64)
    print("不安全反序列化演示(无害载荷)")
    print("=" * 64)

    malicious = pickle.dumps(HarmlessPayload())     # 攻击者构造的恶意 pickle

    line()
    print("[不安全版] pickle.loads 不可信数据:")
    print("  反序列化中会自动执行代码 ↓")
    load_vulnerable(malicious)                       # 这一行会触发 print(无害演示)
    print("  -> 看到上面那行了吗?它是在 loads 时'自动执行'的,真实攻击即 RCE")

    line()
    print("[安全版] 改用 json(同样的'数据'用安全格式传输):")
    data = load_secure('{"user": "alice", "role": "user"}')
    print(f"  json.loads 只还原数据,不执行任何代码: {data}")

    line()
    print("\n结论:pickle/反序列化不可信数据 = RCE;")
    print("优先用 JSON 等只还原数据的格式;必须用 pickle 时,只反序列化可信来源并做签名校验。")
