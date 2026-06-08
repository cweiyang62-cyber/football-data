"""
快速查找剩余8队 - 只试关键渠道
"""
import requests
import json

AF_KEY = "270f70b7e6558bd77dc1fa7239fde118"
AF_BASE = "https://v3.football.api-sports.io"
AF_HEADERS = {"x-apisports-key": AF_KEY}

# 直接用最可能的搜索词
teams_to_find = [
    "Wales", "Ireland", "Peru", "Chile", 
    "Venezuela", "Japan", "Korea", "USA"
]

print("=" * 50)
print("快速查找8队")
print("=" * 50)

for team in teams_to_find:
    print(f"查找 {team}...", end=" ", flush=True)
    try:
        resp = requests.get(
            f"{AF_BASE}/teams",
            headers=AF_HEADERS,
            params={"name": team},
            timeout=8
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results", 0) > 0:
                t = data["response"][0]["team"]
                print(f"[OK] ID={t['id']} ({t['name']})")
            else:
                print("[NOT FOUND]")
        else:
            print(f"[ERR {resp.status_code}]")
    except Exception as e:
        print(f"[ERR] {type(e).__name__}")

print("完成")
