"""
直接获取国际友谊赛数据
"""
import requests
import json
from datetime import datetime
from pathlib import Path

FD_API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
FD_BASE = "https://api.football-data.org/v4"
FD_HEADERS = {"X-Auth-Token": FD_API_KEY}

def get_recent_matches(days=30):
    """获取最近30天国际比赛"""
    try:
        # 获取国际友谊赛数据
        resp = requests.get(
            f"{FD_BASE}/competitions/WC/matches",
            headers=FD_HEADERS,
            params={"dateFrom": "2026-06-01", "dateTo": "2026-06-15"},
            timeout=15
        )
        print(f"WC赛事响应: {resp.status_code}")
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"WC赛事错误: {e}")
    
    return None

def get_team_matches_via_competition(team_name, team_id):
    """通过球队参与的比赛获取战绩"""
    try:
        # 尝试获取球队参与的所有比赛
        resp = requests.get(
            f"{FD_BASE}/teams/{team_id}/matches",
            headers=FD_HEADERS,
            params={"status": "FINISHED", "limit": 10},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("matches", [])
    except Exception as e:
        pass
    return []

def main():
    print("=" * 70)
    print("获取国际比赛数据")
    print("=" * 70)
    
    # 方法1: 通过WC赛事获取
    print("\n[方法1] 通过世界杯预选赛获取...")
    data = get_recent_matches()
    if data:
        matches = data.get("matches", [])
        print(f"找到 {len(matches)} 场比赛")
        
        for m in matches[:5]:
            print(f"  {m.get('utcDate', '')[:10]} | {m.get('homeTeam',{}).get('name')} vs {m.get('awayTeam',{}).get('name')}")
    
    # 方法2: 直接搜索各队近况 - 使用已知数据
    print("\n[方法2] 使用已知热身赛数据生成报告...")
    
    # 基于用户之前提供的数据
    known_data = {
        "荷兰": {
            "最近10场": "6胜3平1负",
            "进球": "28球",
            "失球": "7球",
            "近3场": [
                {"date": "2026-06-04", "对手": "阿尔及利亚", "比分": "0:1", "结果": "负"},
                {"date": "2026-04-01", "对手": "厄瓜多尔", "比分": "1:1", "结果": "平"},
                {"date": "2026-03-28", "对手": "挪威", "比分": "2:1", "结果": "胜"},
            ]
        },
        "法国": {
            "最近10场": "8胜1平1负",
            "进球": "24球",
            "失球": "8球",
            "近3场": [
                {"date": "2026-06-05", "对手": "科特迪瓦", "比分": "1:2", "结果": "负"},
                {"date": "2026-03-30", "对手": "哥伦比亚", "比分": "1:3", "结果": "胜"},
                {"date": "2026-03-27", "对手": "巴西", "比分": "1:2", "结果": "胜"},
            ]
        },
        "巴西": {
            "最近10场": "数据待查",
            "近3场": [
                {"date": "2026-06-05", "对手": "待查", "比分": "待查", "结果": "待查"},
            ]
        },
        "阿根廷": {
            "最近10场": "数据待查",
            "近3场": [
                {"date": "2026-06-05", "对手": "待查", "比分": "待查", "结果": "待查"},
            ]
        },
    }
    
    print("\n已知热身赛数据:")
    for team, data in known_data.items():
        print(f"\n{team}:")
        print(f"  近10场: {data['最近10场']}")
        print(f"  进球: {data['进球']}, 失球: {data['失球']}")
        for m in data.get("近3场", []):
            print(f"  {m['date']} vs {m['对手']}: {m['比分']} ({m['结果']})")
    
    return known_data

if __name__ == "__main__":
    main()
