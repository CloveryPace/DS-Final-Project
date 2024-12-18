from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.team_model import TeamModel
from models.userteam_model import UserTeamModel
from config.config import get_postgres_connection

team_bp = Blueprint('team', __name__)
user_model = UserModel(get_postgres_connection)
team_model = TeamModel(get_postgres_connection)
userteam_model = UserTeamModel(get_postgres_connection)

@team_bp.route('/create', methods=['POST'])
def create_team():
    data = request.json
    if not data.get('team_name'):
        return jsonify({"error": "Team name is required"}), 400
    
    existing_team = team_model.get_team(data['team_name'])
    if existing_team:
        return jsonify({"error": f"Team '{data['team_name']}' already exists"}), 409

    team = team_model.create_team(data['team_name'])
    return jsonify({"message": "Team created successfully", "team_id": str(team.inserted_id)}), 201

@team_bp.route('/<team_name>/add_member', methods=['POST'])
def add_member(team_name):
    data = request.json
    if not data.get('username'):
        return jsonify({"error": "Username is required"}), 400
    
    team = team_model.get_team(team_name)
    if not team:
        return jsonify({"error": f"Team '{team_name}' not found"}), 404
    
    user = user_model.get_user(data['username'])
    if not user:
        return jsonify({"error": f"User '{data['username']}' not found. Please register first."}), 404

    userteam_model.create_user_team(team_name, data['username'])
    return jsonify({"message": f"User '{data['username']}' added to team '{team_name}'"}), 200
