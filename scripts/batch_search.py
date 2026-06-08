"""
批量查询世界杯参赛球队ID
"""
import requests
import time

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def search_in_competition(keyword, competition_code):
    """在指定赛事中搜索球队"""
    headers = {"X-Auth-Token": API_KEY}
    
    try:
        resp = requests.get(
            f"{BASE_URL}/competitions/{competition_code}/teams",
            headers=headers,
            timeout=10
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
        print(f"  [WARN] {competition_code}: {e}")
    return None

def find_team_id(keyword):
    """查找球队ID"""
    # 优先搜索世界杯
    competitions = ["WC", "EC", "CL", "PL", "BL1", "PD", "SA", "FL1"]
    
    for comp in competitions:
        result = search_in_competition(keyword, comp)
        if result:
            return result
    return None

# 待查询球队列表
pending_teams = [
    "Mexico", "USA", "Canada", "Japan", "Korea", 
    "Iran", "Saudi", "Australia", "Qatar", "Uzbekistan",
    "Colombia", "Ecuador", "Peru", "Chile", "Paraguay", "Venezuela",
    "Poland", "Ukraine", "Czech", "Austria", "Hungary", "Romania",
    "Serbia", "Slovakia", "Slovenia", "Greece", "Turkey",
    "Norway", "Sweden", "Denmark", "Switzerland", "Finland",
    "Iceland", "Ireland", "Scotland", "Wales", "Algeria", "Morocco",
    "Egypt", "Nigeria", "Cameroon", "Senegal", "Ghana", "Cote d'Ivoire"
]

print("=" * 60)
print("批量查询世界杯参赛球队ID")
print("=" * 60)

results = {}
for team in pending_teams:
    print(f"查询: {team}...", end=" ")
    result = find_team_id(team)
    if result:
        print(f"[OK] ID={result['id']} ({result['tla']})")
        results[team] = result
    else:
        print("[NOT FOUND]")
    time.sleep(0.5)  # 避免请求过快

print("\n" + "=" * 60)
print(f"完成! 找到 {len(results)}/{len(pending_teams)} 个球队")
print("=" * 60)

# 输出结果供复制
print("\nconfig.yaml 格式:")
for team, data in results.items():
    print(f'    "{team}": {data["id"]},')
