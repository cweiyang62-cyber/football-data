"""
最终9队查询 - 通过不同渠道
"""
import requests
import time

# 这9队使用Football-data的历史ID（基于常见模式）
# 由于API限制，使用占位符，实际使用时需验证

# 通过多次尝试不同的league ID
API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"  # 切换到football-data备用
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# 尝试不同的联赛
def try_football_data(name):
    leagues = ["WC", "EC", "CL", "BL1", "PL", "PD", "SA", "FL1"]
    for league in leagues:
        try:
            resp = requests.get(
                f"{BASE_URL}/competitions/{league}/teams",
                headers=HEADERS, timeout=10
            )
            if resp.status_code == 200:
                for team in resp.json().get("teams", []):
                    if name.lower() in team.get("name", "").lower():
                        return team["id"], team["name"]
        except:
            pass
    return None, None

remaining = [
    "Wales", "Ireland", "Peru", "Chile", "Paraguay", 
    "Venezuela", "Japan", "Korea", "United States"
]

print("通过Football-data备用查询...")
for name in remaining:
    print(f"查询 {name}...", end=" ", flush=True)
    team_id, team_name = try_football_data(name)
    if team_id:
        print(f"[OK] ID={team_id} ({team_name})")
    else:
        print("[NOT FOUND]")
    time.sleep(0.3)
