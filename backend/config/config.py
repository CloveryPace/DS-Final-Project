from pymongo import MongoClient
import redis
import os

class Config:
    # MongoDB 設定
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "marketing_event_db")
    
    # Redis 設定
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

# MongoDB 初始化
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

# Redis 初始化
redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=Config.REDIS_DB, 
    decode_responses=True
)
