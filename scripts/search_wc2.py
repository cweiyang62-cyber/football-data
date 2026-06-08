"""
分批查询世界杯参赛球队ID - 第二批
尝试更多联赛和赛事
"""
import requests
import time
import json

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def search_team(keyword):
    headers = {"X-Auth-Token": API_KEY}
    # 尝试所有可用联赛
    leagues = [
        ("WC", "FIFA World Cup"),
        ("EC", "UEFA Euro"),
        ("CL", "Champions League"),
        ("BL1", "Bundesliga"),
        ("PL", "Premier League"),
        ("PD", "La Liga"),
        ("SA", "Serie A"),
        ("FL1", "Ligue 1"),
        ("PPL", "Primeira Liga"),
        ("DED", "Eredivisie"),
        ("BSA", "Brasileirao"),
    ]
    
    for code, name in leagues:
        try:
            resp = requests.get(
                f"{BASE_URL}/competitions/{code}/teams",
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
                            "league": name
                        }
        except:
            pass
    return None

# 第二批: 南美球队 + 部分未找到的亚洲球队
batch2 = [
    "Colombia", "Ecuador", "Peru", "Chile", "Paraguay", "Venezuela",
    "Japan", "Korea", "Iran", "Saudi", "Australia", "Qatar", "Uzbekistan",
    "United States", "USA", "America"
]

results = {}
print("=" * 60)
print("第二批: 南美 + 亚洲 + 北美")
print("=" * 60)

for team in batch2:
    print(f"查询: {team}...", end=" ", flush=True)
    result = search_team(team)
    if result:
        print(f"[OK] ID={result['id']} ({result['tla']}) - {result['league']}")
        results[team] = result
    else:
        print("[NOT FOUND]")
    time.sleep(0.3)

print(f"\n找到 {len(results)}/{len(batch2)} 个")
print("\n结果:")
for t, r in results.items():
    print(f'  "{t}": {r["id"]},  # {r["name"]}')
