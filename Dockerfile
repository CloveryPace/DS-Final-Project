# 使用 Python 官方映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製程式碼到容器中
COPY websocket_server.py /app/
COPY update_score.py /app/

# 安裝必要套件
RUN pip install redis websockets

# 暴露 WebSocket 服務器埠
EXPOSE 6789

# 啟動 WebSocket 服務器
CMD ["python", "websocket_server.py"]
