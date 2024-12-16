from flask import Blueprint, request, jsonify
from models.score_model import ScoreModel
from config.config import db

score_bp = Blueprint('score', __name__)
score_model = ScoreModel(db)

@score_bp.route('/upload', methods=['POST'])
def upload_score():
    data = request.json
    if not data.get('team_id') or not data.get('user_id') or not data.get('photo_url') or not data.get('checkin_time'):
        return jsonify({"error": "All fields are required"}), 400

    score_model.upload_score(data['team_id'], data['user_id'], data['photo_url'], data['checkin_time'])
    return jsonify({"message": "Score uploaded successfully"}), 201

@score_bp.route('/calculate', methods=['POST'])
def calculate_score():
    data = request.json
    alpha = data.get('alpha', 1)
    beta = data.get('beta', 1)

    team_score = score_model.calculate_team_score(data['team_id'], alpha, beta)
    if team_score:
        return jsonify({"team_id": data['team_id'], "score": team_score['score']}), 200
    return jsonify({"error": "Team not found"}), 404
