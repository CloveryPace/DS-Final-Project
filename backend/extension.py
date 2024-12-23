from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")  # 初始化 socketio 實例
