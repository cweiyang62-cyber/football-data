"""
分批查询世界杯参赛球队ID - 第三批
欧洲其他球队
"""
import requests
import time

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def search_team(keyword):
    headers = {"X-Auth-Token": API_KEY}
    leagues = [
        ("WC", "FIFA World Cup"), ("EC", "UEFA Euro"), ("CL", "Champions League"),
        ("BL1", "Bundesliga"), ("PL", "Premier League"), ("PD", "La Liga"),
        ("SA", "Serie A"), ("FL1", "Ligue 1"), ("PPL", "Primeira Liga"),
        ("DED", "Eredivisie"), ("BSA", "Brasileirao"),
    ]
    for code, name in leagues:
        try:
            resp = requests.get(f"{BASE_URL}/competitions/{code}/teams",
                              headers=headers, timeout=15)
            if resp.status_code == 200:
                for team in resp.json().get("teams", []):
                    if keyword.lower() in team.get("name", "").lower():
                        return {"name": team["name"], "tla": team["tla"], 
                                "id": team["id"], "league": name}
        except:
            pass
    return None

# 第三批: 欧洲球队
batch3 = ["Poland", "Ukraine", "Czech", "Austria", "Hungary", "Romania",
          "Serbia", "Slovakia", "Slovenia", "Greece", "Turkey", "Norway", 
          "Sweden", "Denmark", "Switzerland", "Finland", "Iceland", 
          "Scotland", "Wales", "Ireland", "Algeria", "Morocco", "Egypt",
          "Nigeria", "Cameroon", "Senegal", "Ghana", "Ivory Coast"]

results = {}
print("=" * 60)
print("第三批: 欧洲 + 非洲球队")
print("=" * 60)

for team in batch3:
    print(f"查询: {team}...", end=" ", flush=True)
    result = search_team(team)
    if result:
        print(f"[OK] ID={result['id']} ({result['tla']})")
        results[team] = result
    else:
        print("[NOT FOUND]")
    time.sleep(0.25)

print(f"\n找到 {len(results)}/{len(batch3)} 个")
for t, r in results.items():
    print(f'  "{t}": {r["id"]},  # {r["name"]}')
