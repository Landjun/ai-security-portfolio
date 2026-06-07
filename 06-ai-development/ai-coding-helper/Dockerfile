# 码小安 Web 服务镜像(对标 B3:容器化部署)
# 构建:  docker build -t coding-helper .
# 运行:  docker run -p 8000:8000 --env-file .env coding-helper
# 然后浏览器打开 http://127.0.0.1:8000

FROM python:3.12-slim

WORKDIR /app

# 先装依赖(利用 Docker 层缓存:requirements 不变就不重装)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝代码
COPY . .

# 说明:默认纯对话 Web 服务即可运行;--safe 护栏依赖仓库 02 模块,
# 容器只含本目录,故容器内不启用护栏(见 README 部署说明)。
EXPOSE 8000

CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]
