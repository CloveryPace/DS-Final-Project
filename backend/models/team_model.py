from pymongo import MongoClient
from datetime import datetime

class TeamModel:
    def __init__(self, db):
        self.collection = db["teams"]

    def create_team(self, team_name):
        team = {
            "team_name": team_name
        }
        return self.collection.insert_one(team)

    def get_team(self, team_name):
        return self.collection.find_one({"team_name": team_name})
