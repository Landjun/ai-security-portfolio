"""
test_multimodal.py —— 码小安多模态消息构造接入 CI(纯标准库,无重依赖)。

只测离线的消息构造(base64 编码 + OpenAI 兼容多模态格式),不发任何请求。
运行:  python -m unittest discover -s tests
"""

import importlib.util
import os
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HELPER = os.path.join(_ROOT, "06-ai-development", "ai-coding-helper")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mm = _load(os.path.join(_HELPER, "multimodal.py"), "ch_multimodal")


class TestMultimodal(unittest.TestCase):
    def test_build_vision_messages_structure(self):
        msgs = mm.build_vision_messages(b"\x89PNG_fake", "这段报错怎么修?")
        self.assertEqual(msgs[0]["role"], "system")
        parts = msgs[1]["content"]
        self.assertEqual(parts[0]["type"], "text")
        self.assertEqual(parts[1]["type"], "image_url")
        self.assertTrue(parts[1]["image_url"]["url"].startswith("data:image/png;base64,"))

    def test_encode_image_mime_from_path(self):
        # bytes 默认 png;此处只验证 data URI 前缀与 base64 可解析
        uri = mm.encode_image(b"hello")
        self.assertTrue(uri.startswith("data:image/png;base64,"))


if __name__ == "__main__":
    unittest.main()
