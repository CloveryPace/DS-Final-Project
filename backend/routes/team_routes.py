from flask import Blueprint, request, jsonify
from models.team_model import TeamModel
from config.config import db

team_bp = Blueprint('team', __name__)
team_model = TeamModel(db)

@team_bp.route('/create', methods=['POST'])
def create_team():
    data = request.json
    if not data.get('team_name') or not data.get('member_ids'):
        return jsonify({"error": "Team name and members are required"}), 400

    team = team_model.create_team(data['team_name'], data['member_ids'])
    return jsonify({"message": "Team created successfully", "team_id": str(team.inserted_id)}), 201

@team_bp.route('/<team_name>/add_member', methods=['POST'])
def add_member(team_name):
    data = request.json
    if not data.get('member_id'):
        return jsonify({"error": "Member ID is required"}), 400

    team_model.add_member_to_team(team_name, data['member_id'])
    return jsonify({"message": f"Member added to team {team_name}"}), 200
