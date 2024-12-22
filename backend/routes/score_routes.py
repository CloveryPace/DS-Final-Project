from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from services.score_service import ScoreService
from config.config import get_postgres_connection
from datetime import datetime, timezone

score_bp = Blueprint('score', __name__)

user_model = UserModel(get_postgres_connection)
ACTIVITY_START_TIME = datetime(2024, 6, 1, 0, 0, 0)
score_service = ScoreService(
    activity_start_time=ACTIVITY_START_TIME, alpha=0.01, beta=300)


@score_bp.route('/update', methods=['POST'])
def update_posted_at():
    data = request.json
    if not data or not data.get("username"):
        return jsonify({"error": "Username is required"}), 400

    posted_time = datetime.now(timezone.utc)

    try:
        result = user_model.update_posted_at(data["username"], posted_time)
        message = result.get("message")
        return jsonify({
            "message": message,
            "posted_at": posted_time.isoformat()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # if result.matched_count == 0:
    #     return jsonify({"error": f"User '{data['username']}' not found"}), 404


@score_bp.route('/calculate_score', methods=['POST'])
def calculate_score():
    data = request.json
    if not data or not data.get("team_name"):
        return jsonify({"error": "Team name is required"}), 400

    try:
        result = score_service.calculate_team_score(data["team_name"])
        return jsonify({
            "team_name": result["team_name"],
            "score": result["score"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
