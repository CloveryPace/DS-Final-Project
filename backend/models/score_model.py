from pymongo import MongoClient
from datetime import datetime

class ScoreModel:
    def __init__(self, db):
        self.collection = db["scores"]

    def upload_score(self, team_id, user_id, photo_url, checkin_time):
        score = {
            "team_id": team_id,
            "user_id": user_id,
            "photo_url": photo_url,
            "checkin_time": checkin_time,
            "created_at": datetime.utcnow(),
        }
        return self.collection.insert_one(score)

    def calculate_team_score(self, team_id, alpha, beta):
        # 計算團隊分數，根據人數 (T)、時間差 (S)、新會員數量 (N)
        pipeline = [
            {"$match": {"team_id": team_id}},
            {"$group": {
                "_id": "$team_id",
                "member_count": {"$sum": 1},
                "first_checkin": {"$min": "$checkin_time"},
                "last_checkin": {"$max": "$checkin_time"}
            }},
            {"$project": {
                "score": {
                    "$multiply": [
                        "$member_count",
                        {"$divide": [
                            {"$add": [{"$subtract": ["$last_checkin", "$first_checkin"]}, 1]},
                            alpha
                        ]},
                        beta
                    ]
                }
            }}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else None
