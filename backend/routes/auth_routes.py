from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from models.userteam_model import userteam_model
from models.user_model import user_model
from config.config import get_postgres_connection, release_postgres_connection
from werkzeug.security import generate_password_hash, check_password_hash
from services.score_service import ScoreService
from extension import socketio

auth_bp = Blueprint('auth', __name__)
# user_model = UserModel(get_postgres_connection)
# userteam_model = UserTeamModel(get_postgres_connection)

ACTIVITY_START_TIME = datetime(2024, 6, 1, 0, 0, 0)
score_service = ScoreService(ACTIVITY_START_TIME)


@auth_bp.route('/', methods=['GET'])
def get_all_users():
    try:
        users = user_model.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email and password are required"}), 400

    try:
        password_hash = generate_password_hash(data['password'])
        result = user_model.create_user(
            data['username'], data['email'], password_hash)
        return jsonify(result), 201
    except ValueError as e:
        # 處理用戶已存在的錯誤
        return jsonify({"error": str(e)}), 409
    except RuntimeError as e:
        # 處理資料庫異常
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # 捕捉其他未知錯誤
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    try:
        user = user_model.get_user_by_username(data.get('username'))
    except Exception as e:
        raise e

    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "user": user}), 200


# @auth_bp.route('/post', methods=['POST'])
# def update_posted_at():
#     data = request.json
#     if not data or not data.get("username"):
#         return jsonify({"error": "Username is required"}), 400

#     posted_time = datetime.now(timezone.utc)
#     username = data.get("username")
#     try:
#         user_model.update_posted_at(username, posted_time)
#         # return jsonify({
#         #     "message": f"{result["message"]}",
#         #     "posted_at": posted_time.isoformat()
#         # }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     try:
#         teams = userteam_model.get_teams_by_user(username)
#         for team in teams:
#             score_service.calculate_team_score(team["team_name"])
#         top_teams = userteam_model.get_top_teams()
#         socketio.emit('update_leaderboard', top_teams)
#         return jsonify({"message": f"{username} updated post!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
