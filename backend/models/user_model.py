from pymongo import MongoClient
from datetime import datetime

class UserModel:
    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, username, email, password_hash):
        user = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
            "posted_at": None
        }
        return self.collection.insert_one(user)
    
    def update_posted_at(self, username, posted_time):
        return self.collection.update_one(
            {"username": username},
            {"$set": {"posted_at": posted_time}}
        )
    
    def get_user(self, username):
        return self.collection.find_one({"username": username})
    
    def get_email(self, email):
        return self.collection.find_one({"email": email})
