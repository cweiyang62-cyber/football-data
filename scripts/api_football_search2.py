"""
API-Football 第二批查询 - 用不同搜索词
"""
import requests
import time

API_KEY = "270f70b7e6558bd77dc1fa7239fde118"
BASE_URL = "https://v3.football.api-sports.io"

headers = {"x-apisports-key": API_KEY}

def search_team(name):
    try:
        resp = requests.get(f"{BASE_URL}/teams", headers=headers, params={"name": name}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results", 0) > 0:
                return data["response"][0]["team"]["id"], data["response"][0]["team"]["name"]
    except:
        pass
    return None, None

# 换不同搜索词
batch2 = [
    # 欧洲
    ("Turkey", ["Turkey", "Turkiye", "Türk"]),
    ("Scotland", ["Scotland", "Scot", "Scottish"]),
    ("Wales", ["Wales", "Welsh"]),
    ("Ireland", ["Ireland", "Republic", "Eire"]),
    
    # 南美 - 用国家码
    ("Peru", ["Peru", "Peruvian"]),
    ("Chile", ["Chile", "Chilean"]),
    ("Paraguay", ["Paraguay", "Paraguayan"]),
    ("Venezuela", ["Venezuela", "Venezuelan"]),
    
    # 亚洲
    ("Japan", ["Japan", "Japanese"]),
    ("South Korea", ["Korea", "Korean", "Korea Republic"]),
    ("Iran", ["Iran", "Iranian", "Persia"]),
    ("Qatar", ["Qatar", "Qatari"]),
    ("Uzbekistan", ["Uzbekistan", "Uzbek"]),
    ("USA", ["United States", "Estados Unidos", "America"]),
    
    # 非洲
    ("Algeria", ["Algeria", "Algerian"]),
]

print("=" * 60)
print("第二批查询 - 换搜索词")
print("=" * 60)

results = {}
for orig_name, search_names in batch2:
    found = False
    for search_name in search_names:
        print(f"尝试: {orig_name} -> '{search_name}'...", end=" ", flush=True)
        team_id, team_name = search_team(search_name)
        if team_id:
            print(f"[OK] ID={team_id} ({team_name})")
            results[orig_name] = {"id": team_id, "name": team_name}
            found = True
            break
        else:
            print("[重试]")
    if not found:
        print(f"  {orig_name}: 全部失败")

print(f"\n找到 {len(results)}/{len(batch2)} 个")
