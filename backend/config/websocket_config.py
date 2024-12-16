from flask_socketio import SocketIO

# Socket.IO 設定
socketio = SocketIO(
    cors_allowed_origins="*",  # 允許所有來源跨域請求
    async_mode='threading'     # 使用 threading 模式
)
