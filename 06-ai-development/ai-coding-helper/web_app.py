"""
web_app.py —— 把「码小安」做成 Web 服务(对标教程的 AI 服务化 / SSE 流式 / 前端）。

提供:
    GET  /            返回极简聊天前端页面(static/index.html)
    POST /api/chat    SSE 流式接口:逐段推送模型回答(text/event-stream)
    GET  /api/health  健康检查

按 session_id 区分多会话记忆(对标 @MemoryId)。已开启 CORS,方便前后端分离调试。

运行:
    pip install -r requirements.txt
    cd 06-ai-development/ai-coding-helper
    copy .env.example .env   # 填入 DEEPSEEK_API_KEY
    uvicorn web_app:app --reload --port 8000
    浏览器打开 http://127.0.0.1:8000
"""

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from ai_coding_helper import AiCodingHelper

load_dotenv()  # 读取本目录 .env 里的 DEEPSEEK_API_KEY

_HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = os.path.join(_HERE, "static", "index.html")

app = FastAPI(title="AI 编程小助手 · 码小安")

# 跨域:允许前端从任意源调用(对标教程的「后端支持跨域」)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 单例助手:纯流式对话 + 多会话记忆。如需 RAG/护栏可在此传参开启。
helper = AiCodingHelper(retriever=None, use_tools=False, guardrails=False)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "web-default"


@app.get("/")
def index():
    return FileResponse(INDEX_HTML)


@app.get("/api/health")
def health():
    return {"status": "ok", "model": "deepseek-chat"}


@app.get("/api/metrics")
def metrics():
    """可观测性:聚合最近的对话日志(总轮次/平均延迟/总 token/总成本)。"""
    import observability as obs
    return obs.summarize()


@app.post("/api/chat")
def chat(req: ChatRequest):
    """SSE 流式:把 helper.stream_reply 的每段增量包成 SSE 事件推给前端。"""

    def event_stream():
        try:
            for delta in helper.stream_reply(req.session_id, req.message):
                # JSON 编码以安全携带换行等字符
                yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"
        except Exception as e:  # 出错也通过 SSE 告知前端,避免连接悬挂
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
