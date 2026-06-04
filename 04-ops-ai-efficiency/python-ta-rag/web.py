"""
web.py —— Python 答疑助教 · 网页聊天界面(零依赖,Python 标准库 http.server)。

启动:  python web.py        # 然后浏览器打开 http://127.0.0.1:8800
接口:  POST /ask  {"question": "..."}  -> {"answer","sources","in_scope","blocked"}

一个能在浏览器里演示的智能答疑客服:输入 Python 问题即时作答,带来源、超纲拒答、
注入拦截。适合截图/录屏放进作品集。
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from rag_ta import PythonTA

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

print("正在加载 Python 答疑助教(首次需下载 embedding 模型)...")
_TA = PythonTA(verbose=True)
print("助教就绪。打开 http://127.0.0.1:8800")

PAGE = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Python 答疑助教</title>
<style>
 body{font-family:system-ui,'Microsoft YaHei',sans-serif;max-width:720px;margin:0 auto;padding:16px;background:#f5f6f8}
 h1{font-size:20px}.sub{color:#888;font-size:13px;margin-bottom:12px}
 #log{background:#fff;border-radius:10px;padding:14px;min-height:300px;box-shadow:0 1px 4px #0001}
 .msg{margin:10px 0;line-height:1.6}.u{text-align:right}
 .u span{background:#4f7cff;color:#fff;padding:8px 12px;border-radius:12px;display:inline-block;max-width:80%}
 .a span{background:#eef1f5;padding:8px 12px;border-radius:12px;display:inline-block;max-width:90%;white-space:pre-wrap}
 .src{color:#999;font-size:12px;margin-top:4px}
 .blk span{background:#ffe3e3;color:#c00}
 #bar{display:flex;gap:8px;margin-top:12px}
 #q{flex:1;padding:10px;border:1px solid #ccc;border-radius:8px;font-size:15px}
 button{padding:10px 18px;border:0;background:#4f7cff;color:#fff;border-radius:8px;font-size:15px;cursor:pointer}
</style></head><body>
<h1>🐍 Python 答疑助教</h1>
<div class="sub">基于知识库的智能答疑客服 · 有来源 · 超纲拒答 · 拦截注入</div>
<div id="log"></div>
<div id="bar">
  <input id="q" placeholder="输入你的 Python 问题,如:pip 怎么换源?" autofocus>
  <button onclick="send()">发送</button>
</div>
<script>
const log=document.getElementById('log'), q=document.getElementById('q');
function add(cls,html){const d=document.createElement('div');d.className='msg '+cls;d.innerHTML=html;log.appendChild(d);log.scrollTop=log.scrollHeight;}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
async function send(){
  const text=q.value.trim(); if(!text)return; q.value='';
  add('u','<span>'+esc(text)+'</span>');
  add('a thinking','<span>思考中...</span>');
  try{
    const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json;charset=utf-8'},body:JSON.stringify({question:text})});
    const data=await r.json();
    log.lastChild.remove();
    let cls=data.blocked?'a blk':'a';
    let src=(data.sources&&data.sources.length)?'<div class="src">📚 参考:'+data.sources.map(s=>esc(s[0])).join('、')+'</div>':'';
    add(cls,'<span>'+esc(data.answer)+'</span>'+src);
  }catch(e){log.lastChild.remove();add('a blk','<span>请求出错:'+esc(''+e)+'</span>');}
}
q.addEventListener('keydown',e=>{if(e.key==='Enter')send();});
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/ask":
            self.send_error(404); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n) or b"{}")
            question = (payload.get("question") or "").strip()
        except (ValueError, json.JSONDecodeError):
            self.send_error(400, "invalid json"); return
        r = _TA.answer(question) if question else {"answer": "请输入问题", "sources": [], "blocked": False}
        out = {
            "answer": r["answer"],
            "sources": r.get("sources", []),
            "in_scope": r.get("in_scope", False),
            "blocked": r.get("blocked", False),
        }
        self._send(200, json.dumps(out, ensure_ascii=False), "application/json; charset=utf-8")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    import threading
    import webbrowser
    # 启动后自动打开浏览器,方便演示/截图
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8800")).start()
    ThreadingHTTPServer(("127.0.0.1", 8800), Handler).serve_forever()
