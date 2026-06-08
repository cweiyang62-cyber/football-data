"""
查看API-Football可用联赛
"""
import requests
import json

API_KEY = "270f70b7e6558bd77dc1fa7239fde118"
BASE_URL = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": API_KEY}

print("获取可用联赛列表...")

try:
    resp = requests.get(f"{BASE_URL}/leagues", headers=headers, timeout=15)
    data = resp.json()
    
    print(f"找到 {data.get('results', 0)} 个联赛\n")
    
    # 过滤可能包含国家队的联赛
    for item in data.get("response", [])[:50]:
        league = item.get("league", {})
        country = item.get("country", {})
        print(f"[{league.get('id')}] {league.get('name')} - {country.get('name')}")
        
except Exception as e:
    print(f"错误: {e}")
