from pymongo import MongoClient
from datetime import datetime

class UserTeamModel:
    def __init__(self, db):
        self.collection = db["userteams"]

    def create_user_team(self, team_name, username):
        user_team = {
            "team_name": team_name,
            "username":username
        }
        return self.collection.insert_one(user_team)
    
    def get_users_in_team(self, team_name):
        return list(self.collection.find({"team_name": team_name}))
    
    def count_user_teams(self, username):
        return self.collection.count_documents({"username": username})
    
    def get_teams_by_user(self, username):
        return list(self.collection.find({"username": username}, {"_id": 0, "team_name": 1}))