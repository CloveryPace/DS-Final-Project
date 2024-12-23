from locust import HttpUser, task, between, LoadTestShape
import random
from datetime import datetime
from faker import Faker

fake = Faker()

BASE_URL = "https://flask-backend-1043469906200.asia-east1.run.app"  # 定義基礎 URL


class TestUser(HttpUser):
    def on_start(self):
        """初始化會員資料"""
        username = fake.user_name() + str(random.randint(1000, 9999))
        self.username = username
        self.email = f"{username}@gmail.com"
        self.password = "test"
        self.joined_teams = []
        self.register_user()
        self.login_user()
        self.create_teams_and_join()

    def register_user(self):
        """模擬用戶註冊"""
        response = self.client.post(f"{BASE_URL}/api/auth/register", json={
            "username": self.username,
            "password": self.password,
            "email": self.email
        })
        # if response.status_code == 201:
        #     self.username = username

    def login_user(self):
        """模擬用戶登入"""
        response = self.client.post(f"{BASE_URL}/api/auth/login", json={
            "username": self.username,
            "password": self.password
        })
        # if response.status_code == 200:
        #     self.username = response.json().get("username")

    def create_teams_and_join(self):
        """創建並加入群組"""
        for _ in range(2):  # 每個用戶創建並加入兩個群組
            team_name = fake.word() + str(random.randint(1000, 9999))
            data = {
                "team_name": team_name,
                "username": self.username
            }
            print("建群組 data ", data)
            response = self.client.post(f"{BASE_URL}/api/team/", json=data)
            print("建群組 res ", response.json())
            if response.status_code == 201:
                self.joined_teams.append(team_name)

    @task(10)  # 增加打卡行為的權重
    def post(self):
        """模擬用戶打卡"""
        print(f"打卡的使用者: {self.username}")
        if self.joined_teams:
            team_name = random.choice(self.joined_teams)
            response = self.client.post(f"{BASE_URL}/api/team/{team_name}/post", json={
                "username": self.username,
                "posted_at": datetime.now().isoformat()
            })
            if response.status_code == 200:
                # print(f"成功打卡: 群組 {team_id}")
                pass
            else:
                print('fail', team_name, self.username)
                print(f"打卡失敗: 群組 {response.json()}")

    @task(3)
    def join_team(self):
        """模擬用戶加入群組"""
        try:
            response = self.client.get(f"{BASE_URL}/api/team")
            teams = response.json().get('teams', [])
        except Exception as e:
            print(f"Join team error:  {str(e)}")
        not_joined_team = [
            team for team in teams if team["team_name"] not in self.joined_teams]

        if not_joined_team:
            team_name = random.choice(not_joined_team)["team_name"]
            response = self.client.post(f"{BASE_URL}/api/team/{team_name}/members", json={
                "username": self.username
            })

            if response.status_code == 200:
                print(f"加入群組: {team_name}")
                self.joined_teams.append(team_name)


class IncreasingLoadShape(LoadTestShape):
    """
    模擬越接近結束時間越多人同時打卡的負載形狀。
    """
    total_time = 80  # 測試總時長 (180 秒，即 3 分鐘)
    max_users = 800  # 最大使用者數量

    def tick(self):
        run_time = self.get_run_time()
        if run_time < self.total_time:
            # 使用指數增長模擬接近截止時的流量高峰
            user_count = int(self.max_users *
                             (run_time / self.total_time) ** 2)
            spawn_rate = max(user_count / 10, 0.1)  # 最小生成速度為 0.1
            return (user_count, spawn_rate)
        return None
