import redis
import json

class RedisService:
    def __init__(self, host='localhost', port=6379, db=0):
        """
        初始化 Redis 服務
        :param host: Redis 伺服器位址
        :param port: Redis 連接埠
        :param db: Redis 資料庫索引
        """
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def publish_score_update(self, channel, team_name, score):
        """
        發布即時分數更新到 Redis 頻道
        :param channel: Redis 頻道名稱
        :param team_id: 團隊 ID
        :param score: 最新分數
        """
        message = {
            "team_name": team_name,
            "score": score
        }
        self.redis_client.publish(channel, json.dumps(message))
        print(f"Published to {channel}: {message}")

    def subscribe_to_channel(self, channel):
        """
        訂閱 Redis 頻道並接收訊息
        :param channel: Redis 頻道名稱
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        print(f"Subscribed to channel: {channel}")
        for message in pubsub.listen():
            if message['type'] == 'message':
                print(f"Received message: {json.loads(message['data'])}")