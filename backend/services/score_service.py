from datetime import datetime
from models.user_model import UserModel
from models.team_model import TeamModel
from models.userteam_model import UserTeamModel
from config.config import get_postgres_connection


class ScoreService:
    def __init__(self, activity_start_time, alpha=0.001, beta=1000):
        self.user_model = UserModel(get_postgres_connection)
        self.team_model = TeamModel(get_postgres_connection)
        self.userteam_model = UserTeamModel(get_postgres_connection)
        self.activity_start_time = activity_start_time
        self.alpha = alpha
        self.beta = beta
        # self.redis_client = redis_client
        self.leaderboard_key = "team_scores"

    def calculate_team_score(self, team_name):
        # 找出該 team 所有 user
        try:
            users_in_team = self.userteam_model.get_users_in_team(team_name)
        except Exception as e:
            raise Exception(f"Failed to retrieve users in team: {str(e)}")

        # if not users_in_team:
        #     raise Exception("Team not found or has no members")

        # users_with_null_posted_at = [
        #     user for user in users_in_team if user.get("posted_at") is None]
        # if len(users_with_null_posted_at) > 0:
        #     return 0

        users_posted = [
            user for user in users_in_team if user.get("posted_at") is not None]
        checkin_times = []
        N = 0
        T = 0
        for user_record in users_posted:
            username = user_record["username"]
            # user = self.user_model.get_user_by_username(username)
            if user_record and user_record.get("posted_at"):
                checkin_times.append(user_record["posted_at"])

                participation_count = int(self.userteam_model.count_user_teams(
                    username)["team_count"])
                user_weight = 1 / participation_count if participation_count > 0 else 1
                T += user_weight

                if user_record["created_at"] > self.activity_start_time:
                    N += user_weight

        # if len(checkin_times) < 2:
        #     return {"score": 0, "message": "Not enough check-in records"}

        checkin_times.sort()
        if len(checkin_times) < 2:
            S = 0
        else:
            print(checkin_times[-1])
            print(checkin_times[0])
            S = (checkin_times[-1] - checkin_times[0]).total_seconds()

        print(S)
        score = round((T / (self.alpha *
                            (S + 1))) + (self.beta * N), 5)

        return score
        # return {"team_name": team_name, "score": round(score, 5)}

    # def update_score_cache(self, score):
    #     # 取得更新前的排行榜前20名
    #     old_top_teams = redis_client.zrevrange(
    #         self.leaderboard_key, 0, 19, withscores=True)

    #     # 更新 Redis Sorted Set 中的分數
    #     redis_client.zadd(self.leaderboard_key, {team_name: new_score})

    #     # 取得更新後的排行榜前20名
    #     new_top_teams = redis_client.zrevrange(
    #         self.leaderboard_key, 0, 19, withscores=True)

    #     # 比較舊排行榜和新排行榜
    #     if old_top_teams != new_top_teams:
    #         # 如果排行榜有變化，發布到 Redis Pub/Sub channel
    #         leaderboard = [{"team": team, "score": score}
    #                     for team, score in new_top_teams]
