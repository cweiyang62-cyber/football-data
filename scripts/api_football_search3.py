"""
API-Football 第三批 - 最后9队
通过league搜索尝试
"""
import requests
import time

API_KEY = "270f70b7e6558bd77dc1fa7239fde118"
BASE_URL = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": API_KEY}

# 世界杯预选赛league ID (从API-Football)
WORLD_CUP_LEAGUE_ID = 1

def search_in_league(name, league_id):
    """在指定league中搜索球队"""
    try:
        resp = requests.get(
            f"{BASE_URL}/teams",
            headers=headers,
            params={"name": name, "league": league_id, "season": 2024},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results", 0) > 0:
                team = data["response"][0]["team"]
                return team["id"], team["name"]
    except:
        pass
    return None, None

# 剩余9队 - 用更多变体尝试
remaining = [
    ("Wales", ["Wales", "Welsh National"]),
    ("Ireland", ["Ireland", "Irish", "Republic of Ireland", "Eire"]),
    ("Peru", ["Peru", "Peru National"]),
    ("Chile", ["Chile", "Chile National"]),
    ("Paraguay", ["Paraguay", "Paraguay National"]),
    ("Venezuela", ["Venezuela", "Venezuelan"]),
    ("Japan", ["Japan", "Japan National", "Japanese"]),
    ("South Korea", ["Korea", "South Korea", "Korea Republic"]),
    ("USA", ["USA", "United States", "US", "American", "USA National"]),
]

# 也尝试其他league ID
other_leagues = [
    ("World Cup qualifiers", 6),
    ("Euro qualifiers", 6),
    ("Copa America", 1),  # may not exist
    ("African Cup qualifiers", 5),
]

print("=" * 60)
print("第三批查询 - 最后9队")
print("=" * 60)

results = {}
for orig_name, search_names in remaining:
    found = False
    
    # 先用世界杯league搜索
    for search_name in search_names:
        print(f"[WC] {orig_name} -> '{search_name}'...", end=" ", flush=True)
        team_id, team_name = search_in_league(search_name, WORLD_CUP_LEAGUE_ID)
        if team_id:
            print(f"[OK] ID={team_id} ({team_name})")
            results[orig_name] = {"id": team_id, "name": team_name}
            found = True
            break
        else:
            print("[X]", flush=True)
    
    if not found:
        # 尝试国家队league
        for search_name in search_names:
            print(f"[NT] {orig_name} -> '{search_name}'...", end=" ", flush=True)
            team_id, team_name = search_in_league(search_name, 1)  # try league 1
            if team_id:
                print(f"[OK] ID={team_id} ({team_name})")
                results[orig_name] = {"id": team_id, "name": team_name}
                found = True
                break
            else:
                print("[X]", flush=True)

print(f"\n找到 {len(results)}/{len(remaining)} 个")

# 输出最终结果
print("\n" + "=" * 60)
print("最终汇总:")
print("=" * 60)
for t, r in results.items():
    print(f'  "{t}": {r["id"]},  # {r["name"]}')
