"""
快速测试 Football-data.org API 连接
"""
import requests
import sys

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def test_connection():
    print("=" * 50)
    print("[OK] Football-data.org API 连接测试")
    print("=" * 50)
    
    headers = {"X-Auth-Token": API_KEY}
    
    # 测试1: 获取赛事列表
    print("\n[TEST 1] 获取赛事列表...")
    try:
        resp = requests.get(f"{BASE_URL}/competitions", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        competitions = data.get("competitions", [])
        print(f"[OK] 成功! 共有 {len(competitions)} 个赛事")
        for c in competitions[:5]:
            print(f"   - {c.get('name', 'N/A')} ({c.get('code', 'N/A')})")
    except Exception as e:
        print(f"[FAIL] 失败: {e}")
        return False
    
    # 测试2: 获取球队列表 (英超为例)
    print("\n[TEST 2] 获取英超球队...")
    try:
        resp = requests.get(f"{BASE_URL}/competitions/PL/teams", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        teams = data.get("teams", [])
        print(f"[OK] 成功! 共有 {len(teams)} 支球队")
        for t in teams[:3]:
            print(f"   - {t.get('name', 'N/A')}")
    except Exception as e:
        print(f"[FAIL] 失败: {e}")
    
    # 测试3: 获取荷兰队数据 (2026世界杯参赛队)
    print("\n[TEST 3] 获取荷兰队数据...")
    try:
        resp = requests.get(f"{BASE_URL}/teams/195", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print(f"[OK] 成功! 球队: {data.get('name', 'N/A')}")
        print(f"     简称: {data.get('tla', 'N/A')}")
        print(f"     所在联赛: {data.get('league', {}).get('name', 'N/A')}")
    except Exception as e:
        print(f"[FAIL] 失败: {e}")
    
    print("\n" + "=" * 50)
    print("[DONE] 测试完成!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_connection()
