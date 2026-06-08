"""
查找韩国ID
"""
import requests

AF_KEY = "270f70b7e6558bd77dc1fa7239fde118"
AF_BASE = "https://v3.football.api-sports.io"
AF_HEADERS = {"x-apisports-key": AF_KEY}

for name in ["South Korea", "Korea Republic", "Korea South", "Republic of Korea"]:
    print(f"尝试: {name}...", end=" ", flush=True)
    try:
        resp = requests.get(f"{AF_BASE}/teams", headers=AF_HEADERS, params={"name": name}, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results", 0) > 0:
                t = data["response"][0]["team"]
                print(f"[OK] ID={t['id']} ({t['name']})")
            else:
                print("[NOT FOUND]")
    except Exception as e:
        print(f"[ERR]")
