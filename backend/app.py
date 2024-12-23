from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from routes.auth_routes import auth_bp
from routes.team_routes import team_bp
from config.config import Config
import os
from extension import socketio
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 設定日誌格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化 socketio 與 app
socketio.init_app(app)

# 初始化 sqlalchemy app
# db.init_app(app)

# 註冊路由
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(team_bp, url_prefix='/api/team')


@app.route('/')
def index():
    return "Welcome to the Event Marketing Backend System!"


if __name__ == '__main__':
    print("Starting the Flask Backend...")
    port = int(os.environ.get("PORT", 8080))  # 默認使用 PORT 環境變數，否則默認為 8080
    # app.run(host='0.0.0.0', port=5001, debug=True)
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
