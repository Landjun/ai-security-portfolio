# 录制 30 秒演示 gif(放进 README 顶部,招聘方第一眼看效果)

> 目标:一张 gif 展示「浏览器里向码小安提问 → 答案逐字流式吐出」的真实效果。
> 工具:Windows 推荐 **ScreenToGif**(免费、轻量):https://www.screentogif.com/

## 步骤

1. **起服务**(二选一):
   ```powershell
   # 本地直接跑
   cd 06-ai-development\ai-coding-helper
   uvicorn web_app:app --port 8000
   # 或用 Docker
   docker compose up --build
   ```
   浏览器打开 http://127.0.0.1:8000

2. **打开 ScreenToGif → 录制 → 框选浏览器聊天区域**。

3. **演示脚本(控制在 30 秒内,展示流式是关键)**:
   - 输入:`用 Python 写一个带注释的二分查找` → 回车,等答案逐字流出几行
   - (可选)再问一句:`上一题帮我改成递归版` → 展示**多轮记忆**生效

4. **停止录制 → 编辑**:剪掉头尾空白;若文件偏大,降到 ~10fps、宽度 ≤ 900px、删冗余帧。
   目标 **< 5 MB**(GitHub 单图建议)。

5. **导出为 gif,保存到本目录**:
   ```
   06-ai-development/ai-coding-helper/docs/demo.gif
   ```

6. **启用 README 里的嵌入位**:把 `README.md` 顶部那行注释取消即可:
   ```markdown
   ![码小安 Web 演示](docs/demo.gif)
   ```
   想放到**仓库首页**也展示:在根 `README.md` 的「旗舰项目聚焦 · 码小安」小节加同一行
   (路径改成 `06-ai-development/ai-coding-helper/docs/demo.gif`)。

7. `git add docs/demo.gif README.md && git commit -m "docs: 加码小安演示 gif" && git push`

## 小贴士
- gif 比文字更有说服力,但别超过 5MB,否则 GitHub 加载慢。
- 录之前把浏览器缩放调大、字体清晰;深色背景录出来更"高级"。
- 没装 Docker 也行,本地 `uvicorn` 起即可录。
