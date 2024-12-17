from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import redis
import threading
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Redis 連接
redis_client = redis.StrictRedis(
    host='redis', port=6379, db=0, decode_responses=True)
redis_channel = "leaderboard_updates"
leaderboard_key = "team_scores"  # Redis Sorted Set 的 key


@app.route('/')
def index():
    return "Welcome to the HTTP and WebSocket server!"


# API: 更新團隊分數


@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    team_name = data.get('team_name')
    new_score = data.get('score')

    if not team_name or new_score is None:
        return jsonify({"error": "team_name and score are required"}), 400

    # 取得更新前的排行榜前20名
    old_top_teams = redis_client.zrevrange(
        leaderboard_key, 0, 19, withscores=True)

    # 更新 Redis Sorted Set 中的分數
    redis_client.zadd(leaderboard_key, {team_name: new_score})

    # 取得更新後的排行榜前20名
    new_top_teams = redis_client.zrevrange(
        leaderboard_key, 0, 19, withscores=True)

    # 比較舊排行榜和新排行榜
    if old_top_teams != new_top_teams:
        # 如果排行榜有變化，發布到 Redis Pub/Sub channel
        leaderboard = [{"team": team, "score": score}
                       for team, score in new_top_teams]
        redis_client.publish(redis_channel, json.dumps(leaderboard))
        print("Leaderboard updated and published")
        return jsonify({"message": f"Score updated for {team_name}", "leaderboard": leaderboard})
    else:
        # 排行榜沒有變化，不發布
        print("Leaderboard unchanged. No publish.")
        return jsonify({"message": f"Score updated for {team_name}, but no leaderboard change."})

# 訂閱 Redis channel 並透過 WebSocket 推送


def redis_subscribe():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(redis_channel)
    print(f"Subscribed to Redis channel: {redis_channel}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"New leaderboard data: {message['data']}")
            leaderboard_data = json.loads(message['data'])
            # 發送新排行榜給所有 WebSocket 客戶端
            socketio.emit('update_leaderboard', leaderboard_data)


# 啟動 Redis 訂閱的背景執行緒
threading.Thread(target=redis_subscribe, daemon=True).start()

# WebSocket: 當客戶端連接時


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('server_message', {'data': 'Connected to WebSocket server'})


if __name__ == '__main__':
    print("Starting WebSocket server...")
    socketio.run(app, host='0.0.0.0', port=5000,
                 debug=True, allow_unsafe_werkzeug=True)
