"""
multimodal.py —— 给「码小安」加多模态(看图)能力(B5 补强,对标教程 Multimodality)。

让助手能看**代码截图 / 报错截图 / 架构图**回答问题:按 OpenAI 兼容的多模态消息格式,
把图片编码成 base64 data URI 放进 image_url,与文本一起发给**视觉模型**。

说明:DeepSeek-chat 是纯文本模型,多模态需换**视觉模型**(如阿里 qwen-vl-plus 走 OpenAI 兼容端点,
或任意支持 vision 的 OpenAI 兼容模型)。本文件的消息构造与编码是核心、可离线自测;
真正发请求需配置视觉模型与对应 key/base_url。

用法:
    python multimodal.py --demo <图片路径>   # 干跑:构造并打印多模态消息(不发请求/无需 key)
    python multimodal.py --selftest          # 离线自测消息构造
"""

import base64
import os
import sys

VISION_SYSTEM = "你是编程导师『码小安』,擅长看代码截图、报错截图、架构图,定位问题并给出可运行的修复。"

_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".webp": "image/webp", ".gif": "image/gif"}


def encode_image(image, mime: str = "image/png") -> str:
    """把图片(文件路径或 bytes)编码成 data URI;路径会按扩展名推断 MIME。"""
    if isinstance(image, (bytes, bytearray)):
        raw = bytes(image)
    else:
        mime = _MIME.get(os.path.splitext(image)[1].lower(), "image/png")
        with open(image, "rb") as f:
            raw = f.read()
    b64 = base64.b64encode(raw).decode()
    return f"data:{mime};base64,{b64}"


def build_vision_messages(image, question: str, system: str = VISION_SYSTEM) -> list:
    """构造 OpenAI 兼容的多模态 messages:system + (文本 + 图片) 的 user 消息。"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": encode_image(image)}},
        ]},
    ]


def ask_image(client, model: str, image, question: str) -> str:
    """用视觉模型回答关于图片的问题(client 为 OpenAI 兼容客户端,model 需为视觉模型)。"""
    resp = client.chat.completions.create(
        model=model, messages=build_vision_messages(image, question), temperature=0.3
    )
    return resp.choices[0].message.content


def _self_test():
    """离线自测:消息构造正确(不发请求)。"""
    msgs = build_vision_messages(b"\x89PNG_fake_bytes", "这段报错怎么修?")
    assert msgs[0]["role"] == "system"
    parts = msgs[1]["content"]
    assert parts[0]["type"] == "text" and "报错" in parts[0]["text"]
    assert parts[1]["type"] == "image_url"
    assert parts[1]["image_url"]["url"].startswith("data:image/png;base64,")
    print("multimodal 自测通过:多模态消息(文本 + base64 图片)构造正确。")


def main():
    if "--selftest" in sys.argv:
        _self_test()
        return
    if "--demo" in sys.argv:
        i = sys.argv.index("--demo")
        path = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        if not path or not os.path.exists(path):
            raise SystemExit("用法:python multimodal.py --demo <存在的图片路径>")
        msgs = build_vision_messages(path, "请看图回答:这段代码/报错的问题在哪?")
        url = msgs[1]["content"][1]["image_url"]["url"]
        print("已构造多模态请求(干跑,未发起调用):")
        print(f"  system: {msgs[0]['content'][:30]}...")
        print(f"  user.text: {msgs[1]['content'][0]['text']}")
        print(f"  user.image_url: {url[:48]}... (base64 长度 {len(url)})")
        print("\n要真正作答,请配置视觉模型(如 qwen-vl-plus 的 OpenAI 兼容端点)后调用 ask_image()。")
        return
    print("用法:python multimodal.py --demo <图片路径> | --selftest")


if __name__ == "__main__":
    main()
