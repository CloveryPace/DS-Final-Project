from flask import Blueprint
from flask_socketio import emit
from config.websocket_config import socketio

ws_bp = Blueprint('websocket', __name__)

@socketio.on('update_score')
def update_score(data):
    team_id = data.get('team_id')
    score = data.get('score')
    emit('score_update', {'team_id': team_id, 'score': score}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
