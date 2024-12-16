from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from routes.auth_routes import auth_bp
from routes.team_routes import team_bp
from routes.score_routes import score_bp
from routes.websocket_routes import ws_bp
from config.config import Config
from services.redis_service import RedisService

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(team_bp, url_prefix='/api/team')
app.register_blueprint(score_bp, url_prefix='/api/score')
app.register_blueprint(ws_bp, url_prefix='/api/ws')

redis_service = RedisService()

@app.route('/')
def index():
    return "Welcome to the Event Marketing Backend System!"

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('status', {'message': 'Connected to the server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("Starting the Flask Backend...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
