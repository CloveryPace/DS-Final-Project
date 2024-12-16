from pymongo import MongoClient
from datetime import datetime

class TeamModel:
    def __init__(self, db):
        self.collection = db["teams"]

    def create_team(self, team_name, member_ids):
        team = {
            "team_name": team_name,
            "member_ids": member_ids,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        return self.collection.insert_one(team)

    def find_team_by_name(self, team_name):
        return self.collection.find_one({"team_name": team_name})

    def add_member_to_team(self, team_name, member_id):
        return self.collection.update_one(
            {"team_name": team_name},
            {"$push": {"member_ids": member_id}, "updated_at": datetime.utcnow()}
        )
