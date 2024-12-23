import requests
import random

# 定義基礎 URL
BASE_URL = "http://localhost:8080/api"  # 根據實際情況修改

# 測試數據
users = [
    {"username": "user1", "email": "user1@example.com", "password": "password1"},
    {"username": "user2", "email": "user2@example.com", "password": "password2"},
]

teams = [
    {"team_name": "team1", "username": "user1"},
    {"team_name": "team2", "username": "user2"},
]

# 測試用戶註冊
print("Testing user registration...")
for user in users:
    response = requests.post(f"{BASE_URL}/auth/register", json=user)
    print(f"Registering {user['username']}:",
          response.status_code, response.json())

# 測試獲取所有用戶
print("\nTesting get all users...")
response = requests.get(f"{BASE_URL}/auth/")
print("Get all users:", response.status_code, response.json())

# 測試用戶登錄
print("\nTesting user login...")
for user in users:
    login_data = {"username": user["username"], "password": user["password"]}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Logging in {user['username']}:",
          response.status_code, response.json())

# 測試創建團隊
print("\nTesting create team...")
for team in teams:
    # random_user = random.choice(users)
    # team["username"] = random_user["username"]
    response = requests.post(f"{BASE_URL}/team/", json=team)
    print(f"Creating {team['team_name']}:",
          response.status_code, response.json())

# 測試獲取所有團隊
print("\nTesting get all teams...")
response = requests.get(f"{BASE_URL}/team/")
print("Get all teams:", response.status_code, response.json())

# 測試向團隊添加成員
print("\nTesting add member to team...")
for team in teams:
    member_data = {"username": team["username"]}
    response = requests.post(
        f"{BASE_URL}/team/{team['team_name']}/members", json=member_data)
    print(f"Adding member to {team['team_name']}:",
          response.status_code, response.json())

# 測試獲取團隊成員
print("\nTesting get team members...")
for team in teams:
    response = requests.get(f"{BASE_URL}/team/{team['team_name']}/members")
    print(f"Getting members for {
          team['team_name']}:", response.status_code, response.json())

# 測試更新團隊發佈時間
print("\nTesting update posted_at for team...")
for team in teams:
    post_data = {"username": team["username"]}
    response = requests.post(
        f"{BASE_URL}/team/{team['team_name']}/post", json=post_data)
    print(
        f"Updating post for team '{
            team['team_name']}' by user '{team['username']}':",
        response.status_code,
        response.json(),
    )
