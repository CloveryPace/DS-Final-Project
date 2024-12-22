from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from routes.auth_routes import auth_bp
from routes.team_routes import team_bp
from routes.score_routes import score_bp
from routes.websocket_routes import ws_bp
from config.config import Config
import os
from extension import socketio

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 初始化 socketio 與 app
socketio.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(team_bp, url_prefix='/api/team')
app.register_blueprint(score_bp, url_prefix='/api/score')
app.register_blueprint(ws_bp, url_prefix='/api/ws')


@app.route('/')
def index():
    return "Welcome to the Event Marketing Backend System!"


if __name__ == '__main__':
    print("Starting the Flask Backend...")
    # app.run(host='0.0.0.0', port=5001, debug=True)
    socketio.run(app, host='0.0.0.0', port=os.getenv("PORT", 5000), debug=True)
