"""
通过比赛查找韩国ID
"""
import requests

AF_KEY = "270f70b7e6558bd77dc1fa7239fde118"
AF_BASE = "https://v3.football.api-sports.io"
AF_HEADERS = {"x-apisports-key": AF_KEY}

print("通过比赛查找韩国...")

# 尝试获取包含韩国的比赛
params = {
    "team": "South Korea",
    "last": 5,
    "league": 1
}

try:
    resp = requests.get(
        f"{AF_BASE}/fixtures",
        headers=AF_HEADERS,
        params=params,
        timeout=10
    )
    print(f"状态: {resp.status_code}")
    data = resp.json()
    print(f"结果数: {data.get('results', 0)}")
except Exception as e:
    print(f"错误: {e}")

# 直接猜测ID范围
print("\n尝试常见ID范围...")
common_korea_ids = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

for test_id in common_korea_ids:
    try:
        resp = requests.get(
            f"{AF_BASE}/teams/id/{test_id}",
            headers=AF_HEADERS,
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            team = data.get("response", [{}])[0].get("team", {})
            name = team.get("name", "")
            if "Korea" in name or "South" in name:
                print(f"  ID={test_id}: {name} [MATCH!]")
    except:
        pass

print("\n完成")
