import asyncio
import aiohttp
import random

# 目標 API 端點
url = 'http://localhost:5000/update_score'

# 要發送的 POST 請求的資料
data_list = [{'team_name': f'Team {i}',
              'score': random.randint(1, 10000)} for i in range(1, 10001)]

# 非同步發送 POST 請求的函數


async def send_post_request(session, data):
    try:
        async with session.post(url, json=data) as response:
            res = await response.json()
            print(f"Response: {response.status}, {res}")
    except Exception as e:
        print(f"Error: {str(e)}")

# 使用 asyncio 模擬多個非同步請求


async def simulate_multiple_requests():
    async with aiohttp.ClientSession() as session:
        tasks = [send_post_request(session, data) for data in data_list]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(simulate_multiple_requests())
