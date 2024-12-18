from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from services.score_service import ScoreService
from config.config import get_postgres_connection
from datetime import datetime

score_bp = Blueprint('score', __name__)

user_model = UserModel(get_postgres_connection)
ACTIVITY_START_TIME = datetime(2024, 6, 1, 0, 0, 0)
score_service = ScoreService(activity_start_time=ACTIVITY_START_TIME, alpha=2, beta=3)

@score_bp.route('/update', methods=['POST'])
def update_posted_at():
    data = request.json
    if not data or not data.get("username"):
        return jsonify({"error": "Username is required"}), 400

    posted_time = datetime.utcnow()
    
    result = user_model.update_posted_at(data["username"], posted_time)

    if result.matched_count == 0:
        return jsonify({"error": f"User '{data['username']}' not found"}), 404

    return jsonify({
        "message": f"User '{data['username']}' post time updated successfully",
        "posted_at": posted_time.isoformat()
    }), 200

@score_bp.route('/calculate_score', methods=['POST'])
def calculate_score():
    data = request.json
    if not data or not data.get("team_name"):
        return jsonify({"error": "Team name is required"}), 400

    result = score_service.calculate_team_score(data["team_name"])

    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify({
        "team_name": result["team_name"],
        "score": result["score"]
    }), 200
