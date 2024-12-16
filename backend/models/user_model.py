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
            "updated_at": datetime.utcnow(),
        }
        return self.collection.insert_one(user)

    def find_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def update_user_password(self, email, new_password_hash):
        return self.collection.update_one(
            {"email": email},
            {"$set": {"password_hash": new_password_hash, "updated_at": datetime.utcnow()}}
        )
