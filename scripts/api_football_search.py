"""
使用 API-Football 查询剩余球队ID
正确URL: https://v3.football.api-sports.io
"""
import requests
import time
import json

API_KEY = "270f70b7e6558bd77dc1fa7239fde118"
BASE_URL = "https://v3.football.api-sports.io"

def test_api():
    """测试API连接"""
    print("=" * 60)
    print("[TEST] API-Football 连接测试")
    print("=" * 60)
    
    headers = {"x-apisports-key": API_KEY}
    
    try:
        resp = requests.get(f"{BASE_URL}/status", headers=headers, timeout=15)
        print(f"状态码: {resp.status_code}")
        data = resp.json()
        print(f"账户信息: {json.dumps(data, indent=2)[:500]}")
        return data
    except Exception as e:
        print(f"错误: {e}")
        return None

def search_team(name):
    """通过name参数搜索球队"""
    headers = {"x-apisports-key": API_KEY}
    
    try:
        url = f"{BASE_URL}/teams"
        params = {"name": name}
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", 0)
            if results > 0:
                team = data["response"][0]["team"]
                return {
                    "name": team.get("name"),
                    "id": team.get("id"),
                    "logo": team.get("logo"),
                }
    except Exception as e:
        print(f"  错误: {e}")
    return None

# 待查询的球队列表
pending_teams = [
    # 欧洲
    "Poland", "Romania", "Serbia", "Slovakia", "Greece", "Turkey",
    "Norway", "Finland", "Iceland", "Scotland", "Wales", "Ireland",
    # 南美
    "Peru", "Chile", "Paraguay", "Venezuela",
    # 亚洲
    "Japan", "South Korea", "Iran", "Qatar", "Uzbekistan", "USA",
    # 非洲
    "Algeria", "Morocco", "Egypt", "Nigeria", "Cameroon", 
    "Senegal", "Ghana", "Ivory Coast"
]

if __name__ == "__main__":
    # 先测试API
    print("\n测试API连接...")
    test_result = test_api()
    
    if test_result:
        print("\n" + "=" * 60)
        print("API连接成功! 开始查询剩余球队...")
        print("=" * 60)
        
        results = {}
        for team in pending_teams:
            print(f"查询: {team}...", end=" ", flush=True)
            result = search_team(team)
            if result:
                print(f"[OK] ID={result['id']} ({result['name']})")
                results[team] = result
            else:
                print("[NOT FOUND]")
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print(f"查询完成! 找到 {len(results)}/{len(pending_teams)} 个")
        print("=" * 60)
        
        print("\n结果汇总:")
        for t, r in results.items():
            print(f'  "{t}": {r["id"]},  # {r["name"]}')
        
        # 保存结果
        with open("api_football_results.json", "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("\n结果已保存到 api_football_results.json")
    else:
        print("API连接失败，请检查Key是否有效")
