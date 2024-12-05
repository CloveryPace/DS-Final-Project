import asyncio
import websockets
import redis
import os
import json

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# 連接到 Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)


async def notify_clients():
    async with websockets.serve(handler, "localhost", 6789):
        await asyncio.Future()  # 保持伺服器運行


async def handler(websocket, path):
    while True:
        # 取得前 10 名的團隊排名
        top_teams = redis_client.zrevrange(
            'team_ranking', 0, 19, withscores=True)
        # 傳送給連接的客戶端
        print(f"Sending updated rankings: {top_teams}")  # 確認是否正確發送數據
        await websocket.send(json.dumps(top_teams))
        await asyncio.sleep(1)  # 每 1 秒更新一次

asyncio.run(notify_clients())
