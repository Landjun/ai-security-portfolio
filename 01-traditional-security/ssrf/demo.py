"""
demo.py —— 服务端请求伪造(SSRF)本地演示:不安全 vs 安全。

原理:服务端按用户提供的 URL 发起请求时,若不校验,攻击者可让它访问内网服务、
云元数据(169.254.169.254)、本机管理端口、file:// 本地文件等。

本演示**不真实联网**,用一个模拟 fetch + URL 安全校验函数说明原理,完全本地无害。
运行:  python demo.py
"""

import ipaddress
import urllib.parse

ALLOWED_SCHEMES = {"http", "https"}
BLOCK_HOSTS = {"localhost", "metadata.google.internal", "metadata"}


def _mock_fetch(url):
    return f"[模拟] 已获取 {url} 的响应内容"


def fetch_vulnerable(url):
    """不安全:对任意 URL 直接发起请求。"""
    return _mock_fetch(url)


def is_safe_url(url):
    """安全校验:协议白名单 + 拒绝指向内网/保留地址/本机的目标。"""
    p = urllib.parse.urlparse(url)
    if p.scheme not in ALLOWED_SCHEMES:
        return False, f"协议 {p.scheme!r} 不允许(只允许 http/https)"
    host = (p.hostname or "").lower()
    if host in BLOCK_HOSTS:
        return False, f"目标 {host} 指向本机/元数据服务"
    try:
        ip = ipaddress.ip_address(host)            # host 是 IP 字面量时校验
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False, f"IP {host} 属于内网/保留地址"
    except ValueError:
        pass  # host 是域名;真实实现应解析后再校验(此处演示从略)
    return True, "通过"


def fetch_secure(url):
    ok, reason = is_safe_url(url)
    if not ok:
        return f"[已拦截] {reason}"
    return _mock_fetch(url)


def line():
    print("-" * 64)


if __name__ == "__main__":
    payloads = [
        "https://api.example.com/data",                 # 正常外部
        "http://169.254.169.254/latest/meta-data/",     # 云元数据(SSRF 经典)
        "http://127.0.0.1:8080/admin",                  # 本机管理端口
        "http://192.168.1.1/",                          # 内网
        "file:///etc/passwd",                           # 本地文件
    ]
    print("=" * 64)
    print("SSRF 演示")
    print("=" * 64)
    for url in payloads:
        line()
        print(f"请求 URL: {url}")
        print(f"  [不安全版] {fetch_vulnerable(url)}")
        print(f"  [安全版  ] {fetch_secure(url)}")
    line()
    print("\n结论:不校验 URL = 服务端被当作跳板访问内网/元数据/本机;")
    print("协议白名单 + 拒绝内网/保留地址(域名需解析后校验)是 SSRF 核心防御。")
