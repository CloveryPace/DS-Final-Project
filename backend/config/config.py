from datetime import datetime
import psycopg2
import os
from psycopg2 import pool


class Config:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "35.236.186.232")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12341234")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")


# 初始化連接池
db_pool = pool.SimpleConnectionPool(
    1,  # 最小連接數
    50,  # 最大連接數
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD,
    dbname=Config.POSTGRES_DB,
)


def get_postgres_connection():
    if db_pool:
        return db_pool.getconn()  # 從池中獲取連接
    else:
        raise ConnectionError("Database connection pool is not initialized")


def release_postgres_connection(conn):
    if db_pool:
        db_pool.putconn(conn)  # 釋放連接回池中


# # Redis
# redis_client = redis.StrictRedis(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     db=Config.REDIS_DB,
#     decode_responses=True
# )
