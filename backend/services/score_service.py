from datetime import datetime, timedelta

class ScoreService:
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta

    def calculate_team_score(self, checkin_times, new_member_count):
        """
        計算團隊分數
        :param checkin_times: 打卡時間清單 (list of datetime)
        :param new_member_count: 新會員數量 (int)
        :return: 分數 (float)
        """
        if not checkin_times or len(checkin_times) == 0:
            return 0

        # 排序打卡時間，計算時間差
        checkin_times.sort()
        time_diff = (checkin_times[-1] - checkin_times[0]).total_seconds()

        # 計算團隊人數
        team_size = len(checkin_times)

        # 分數計算公式
        score = (team_size / (self.alpha * (time_diff + 1))) + (self.beta * new_member_count)
        return round(score, 2)

# 測試範例
if __name__ == "__main__":
    service = ScoreService(alpha=2, beta=3)
    checkin_times = [
        datetime(2024, 6, 1, 10, 0, 0),
        datetime(2024, 6, 1, 10, 5, 0),
        datetime(2024, 6, 1, 10, 15, 0)
    ]
    new_members = 2
    score = service.calculate_team_score(checkin_times, new_members)
    print(f"Team Score: {score}")
