import redis
import time
import random
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# 連接到 Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

# 模擬一個上傳事件


def update_team_score(team_id, T, S, N, alpha=1.0, beta=2.0):
    # 計算積分公式
    score = T / (alpha * (S + 1)) + beta * N
    # 使用 Redis 的 Sorted Set 儲存排名
    redis_client.zadd('team_ranking', {team_id: score})
    print(f"Team {team_id} score updated to: {score}")


# 範例：更新三個團隊的積分
for i in range(1000):
    T = random.randint(1, 100)
    S = random.uniform(1, 10)
    N = random.randint(1, T)
    update_team_score(f"Team_{i}", T=T, S=S, N=N)
    time.sleep(2)
# update_team_score("Team_1", T=5, S=10, N=2)
# update_team_score("Team_2", T=3, S=5, N=4)
# update_team_score("Team_3", T=8, S=2, N=1)
