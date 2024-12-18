from datetime import datetime
from models.user_model import UserModel
from models.team_model import TeamModel
from models.userteam_model import UserTeamModel
from config.config import get_postgres_connection

class ScoreService:
    def __init__(self, activity_start_time, alpha=1, beta=1):
        self.user_model = UserModel(get_postgres_connection)
        self.team_model = TeamModel(get_postgres_connection)
        self.userteam_model = UserTeamModel(get_postgres_connection)
        self.activity_start_time = activity_start_time
        self.alpha = alpha
        self.beta = beta

    def calculate_team_score(self, team_name):
        users_in_team = self.userteam_model.get_users_in_team(team_name)
        if not users_in_team:
            return {"error": "Team not found or has no members"}

        checkin_times = []
        new_member_count = 0
        total_weighted_team_size = 0

        for user_record in users_in_team:
            username = user_record["username"]
            user = self.user_model.get_user(username)
            if user and user.get("posted_at"):
                checkin_times.append(user["posted_at"])

                participation_count = self.userteam_model.count_user_teams(username)
                user_weight = 1 / participation_count if participation_count > 0 else 1
                total_weighted_team_size += user_weight

                if user["created_at"] > self.activity_start_time:
                    new_member_count += 1

        if len(checkin_times) < 2:
            return {"score": 0, "message": "Not enough check-in records"}

        checkin_times.sort()
        time_diff = (checkin_times[-1] - checkin_times[0]).total_seconds()

        team_size = len(checkin_times)

        score = (total_weighted_team_size / (self.alpha * (time_diff + 1))) + (self.beta * new_member_count)
        return {"team_name": team_name, "score": round(score, 2)}
