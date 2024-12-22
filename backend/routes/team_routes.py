from datetime import datetime
from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.team_model import TeamModel
from models.userteam_model import UserTeamModel
from config.config import get_postgres_connection
from services.score_service import ScoreService
from extension import socketio

team_bp = Blueprint('team', __name__)
user_model = UserModel(get_postgres_connection)
team_model = TeamModel(get_postgres_connection)
userteam_model = UserTeamModel(get_postgres_connection)
ACTIVITY_START_TIME = datetime(2024, 6, 1, 0, 0, 0)
score_service = ScoreService(ACTIVITY_START_TIME)


@team_bp.route('/', methods=['GET'])
def get_all_teams():
    try:
        teams = team_model.get_all_teams()
        return jsonify({"teams": teams}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching teams: {str(e)}"}), 500


@team_bp.route('/', methods=['POST'])
def create_team():
    data = request.json
    if not data.get('team_name'):
        return jsonify({"error": "Team name is required"}), 400

    try:
        existing_team = team_model.get_team_by_name(data['team_name'])
    except Exception as e:
        return jsonify({"error": f"An error occurred while checking for existing team: {str(e)}"}), 500

    if existing_team:
        return jsonify({"error": f"Team '{data['team_name']}' already exists"}), 409

    try:
        response = team_model.create_team(data['team_name'])
    except Exception as e:
        return jsonify({"error": f"An error occurred while creating the team: {str(e)}"}), 500

    return jsonify({"message": "Team created successfully", "team_id": str(response["team_id"])}), 201


@team_bp.route('/<team_name>/members', methods=['POST'])
def add_member(team_name):
    data = request.json
    if not data.get('username'):
        return jsonify({"error": "Username is required"}), 400

    username = data['username']
    team = team_model.get_team_by_name(team_name)
    if not team:
        return jsonify({"error": f"Team '{team_name}' not found"}), 404

    user = user_model.get_user_by_username(data['username'])
    if not user:
        return jsonify({"error": f"User '{data['username']}' not found. Please register first."}), 404

    userteam_model.add_user_to_team(team_name, data['username'])
    try:
        teams = userteam_model.get_teams_by_user(username)
        print(teams)
        for team in teams:
            score_service.calculate_team_score(team["team_name"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        top_teams = userteam_model.get_top_teams()
        socketio.emit('update_leaderboard', top_teams)
        print(f"{top_teams} emitted")
        return jsonify({"message": f"User '{data['username']}' added to team '{team_name}'"}), 200
        # return jsonify(top_teams), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@team_bp.route('/<team_name>/members', methods=['GET'])
def get_team_members(team_name):
    try:
        team = team_model.get_team_by_name(team_name)
        if not team:
            return jsonify({"error": f"Team '{team_name}' not found"}), 404

        members = userteam_model.get_users_in_team(team_name)
        return jsonify({"members": members}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching team members: {str(e)}"}), 500
