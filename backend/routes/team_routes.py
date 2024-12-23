from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from models.user_model import user_model
from models.team_model import team_model
from models.userteam_model import userteam_model
from services.score_service import ScoreService
from extension import socketio

team_bp = Blueprint('team', __name__)
# user_model = UserModel(get_postgres_connection)
# team_model = TeamModel(get_postgres_connection)
# userteam_model = UserTeamModel(get_postgres_connection)
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
    if not data.get('team_name') or not data.get('username'):
        return jsonify({"error": "Team name and Username are required"}), 400

    team_name = data['team_name']
    username = data['username']
    try:
        existing_team = team_model.get_team_by_name(team_name)
    except Exception as e:
        return jsonify({"error": f"An error occurred while checking for existing team: {str(e)}"}), 500

    if existing_team:
        return jsonify({"error": f"Team '{team_name}' already exists"}), 409

    try:
        response = team_model.create_team(team_name)
        userteam_model.add_user_to_team(team_name, username)
    except Exception as e:
        return jsonify({"error": f"An error occurred while creating the team: {str(e)}"}), 500

    return jsonify({"message": "Team created successfully"}), 201


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
        for team in teams:
            score_service.calculate_team_score(team["team_name"])
        return jsonify({"message": f"User '{data['username']}' added to team '{team_name}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # try:
    #     top_teams = team_model.get_top_teams()
    #     # socketio.emit('update_leaderboard', top_teams)
    #     print(f"{top_teams} emitted")
    #     # return jsonify(top_teams), 200
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


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


@team_bp.route('/<team_name>/post', methods=['POST'])
def update_posted_at(team_name):
    data = request.json
    if not data or not data.get("username"):
        return jsonify({"error": "Username is required"}), 400

    posted_time = datetime.now(timezone.utc)
    username = data.get("username")
    try:
        userteam_model.update_posted_at(username, team_name, posted_time)
        # return jsonify({
        #     "message": f"{result["message"]}",
        #     "posted_at": posted_time.isoformat()
        # }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    score = score_service.calculate_team_score(team_name)
    try:
        team_model.update_team_score(team_name, score)
    except Exception as e:
        raise Exception(f"Failed to update team score: {str(e)}")
    return jsonify({"message": f"{username} updated post! {score}"}), 200


@team_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        top_teams = team_model.get_top_teams()
        return jsonify({"leaderboard": top_teams}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching the leaderboard: {str(e)}"}), 500
