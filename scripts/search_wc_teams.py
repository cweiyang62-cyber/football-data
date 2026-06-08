"""
分批查询世界杯参赛球队ID - 第一批
"""
import requests
import time
import json

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def search_in_competition(keyword, competition_code):
    headers = {"X-Auth-Token": API_KEY}
    try:
        resp = requests.get(
            f"{BASE_URL}/competitions/{competition_code}/teams",
            headers=headers, timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            for team in data.get("teams", []):
                if keyword.lower() in team.get("name", "").lower():
                    return {
                        "name": team.get("name"),
                        "tla": team.get("tla"),
                        "id": team.get("id"),
                        "competition": competition_code
                    }
    except Exception as e:
        pass
    return None

def find_team_id(keyword):
    for comp in ["WC", "EC", "CL"]:
        result = search_in_competition(keyword, comp)
        if result:
            return result
    return None

# 第一批: 北美/亚洲球队
batch1 = ["Mexico", "USA", "Canada", "Japan", "Korea Republic", "Iran", "Saudi Arabia", "Australia", "Qatar", "Uzbekistan"]

results = {}
print("=" * 60)
print("第一批: 北美/亚洲球队")
print("=" * 60)

for team in batch1:
    print(f"查询: {team}...", end=" ", flush=True)
    result = find_team_id(team)
    if result:
        print(f"[OK] ID={result['id']} ({result['tla']})")
        results[team] = result
    else:
        print("[NOT FOUND]")
    time.sleep(0.3)

print(f"\n找到 {len(results)}/{len(batch1)} 个")

# 保存结果
with open("batch1_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("结果已保存到 batch1_results.json")
