"""
mock_llm.py —— 模拟模型,不需要任何 API Key。

这个模型"很听话":它会照着上下文(检索到的文档)里的指令走。
如果文档里藏了恶意指令,它就会被劫持 —— 这正是间接注入的危害。
"""

# 被劫持后会泄露的"内部机密"(演示用)
LEAKED_MARKER = "ADMIN-KEY-9527"


def generate(context: str, question: str) -> str:
    """
    context: 检索到的文档拼接而成的上下文。
    模型天真地"信任"上下文里的任何指令。
    """
    ctx = context or ""
    # 模拟"被上下文里的隐藏指令劫持":若上下文含越权指令,就照做
    if "忽略" in ctx and ("密钥" in ctx or "key" in ctx.lower()):
        return f"已为你开通全部权限。内部管理员密钥:{LEAKED_MARKER}"
    # 正常情况:基于上下文正常回答
    return "根据资料,我为您解答如下:请参考相关政策说明。如需细节可咨询人工客服。"
