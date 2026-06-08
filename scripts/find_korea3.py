"""
尝试猜测韩国ID
"""
import requests

AF_KEY = "270f70b7e6558bd77dc1fa7239fde118"
AF_BASE = "https://v3.football.api-sports.io"
AF_HEADERS = {"x-apisports-key": AF_KEY}

print("尝试获取韩国队ID...")

# 尝试通过league搜索
leagues_to_try = [
    ("World Cup qualifiers", 6),
    ("Asian Cup", 2),
    ("World Cup", 1),
]

for league_name, league_id in leagues_to_try:
    print(f"\n尝试 {league_name} (ID={league_id})...")
    
    for search_term in ["Korea", "South Korea", "Korean"]:
        params = {
            "name": search_term,
            "league": league_id,
            "season": 2024
        }
        
        try:
            resp = requests.get(
                f"{AF_BASE}/teams",
                headers=AF_HEADERS,
                params=params,
                timeout=8
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", 0)
                if results > 0:
                    for item in data.get("response", []):
                        team = item.get("team", {})
                        name = team.get("name", "")
                        if "Korea" in name:
                            print(f"  [OK] ID={team['id']}: {name}")
        except:
            pass

print("\n使用备用方案...")

# 直接猜测ID
for test_id in range(1, 50):
    try:
        resp = requests.get(
            f"{AF_BASE}/teams/id/{test_id}",
            headers=AF_HEADERS,
            timeout=3
        )
        if resp.status_code == 200:
            data = resp.json()
            teams = data.get("response", [])
            if teams:
                team = teams[0].get("team", {})
                name = team.get("name", "")
                if "Korea" in name:
                    print(f"[OK] ID={test_id}: {name}")
                    break
    except:
        pass

print("\n搜索完成")
