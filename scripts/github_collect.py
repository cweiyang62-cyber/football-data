"""
GitHub Actions 专用采集脚本
简化版，依赖最少化
"""
import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# API Keys (从环境变量读取)
FD_KEY = os.environ.get("FD_API_KEY", "c50e3649bded4ee09620aaf8c820a8ac")
AF_KEY = os.environ.get("AF_API_KEY", "270f70b7e6558bd77dc1fa7239fde118")

FD_BASE = "https://api.football-data.org/v4"
AF_BASE = "https://v3.football.api-sports.io"

def get_fd_matches():
    """获取世界杯热身赛"""
    headers = {"X-Auth-Token": FD_KEY}
    try:
        resp = requests.get(
            f"{FD_BASE}/competitions/WC/matches",
            headers=headers,
            params={"dateFrom": "2026-06-01", "dateTo": "2026-06-30"},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json().get("matches", [])
    except Exception as e:
        print(f"FD API 错误: {e}")
    return []

def get_team_fixtures(team_name, team_id):
    """获取球队近况"""
    headers = {"X-Auth-Token": FD_KEY}
    try:
        resp = requests.get(
            f"{FD_BASE}/teams/{team_id}/matches",
            headers=headers,
            params={"status": "FINISHED", "limit": 10},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            matches = data.get("matches", [])
            result = {
                "team": team_name,
                "fixtures": []
            }
            for m in matches[:10]:
                result["fixtures"].append({
                    "date": m.get("utcDate", "")[:10],
                    "home": m.get("homeTeam", {}).get("name", ""),
                    "away": m.get("awayTeam", {}).get("name", ""),
                    "score": m.get("score", {}).get("fullTime", {}),
                    "status": m.get("status", ""),
                })
            return result
    except Exception as e:
        print(f"  {team_name}: {e}")
    return None

def main():
    print("=" * 60)
    print("GitHub Actions - 自动数据采集")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # 获取热身赛
    print("\n[1/2] 获取热身赛数据...")
    matches = get_fd_matches()
    print(f"  找到 {len(matches)} 场比赛")
    
    # 保存热身赛
    cache_dir = Path(__file__).parent.parent / "cache"
    cache_dir.mkdir(exist_ok=True)
    
    matches_data = {
        "采集时间": datetime.now().isoformat(),
        "总计": len(matches),
        "比赛": [
            {
                "date": m.get("utcDate", "")[:10],
                "home": m.get("homeTeam", {}).get("name", ""),
                "away": m.get("awayTeam", {}).get("name", ""),
                "score": m.get("score", {}).get("fullTime", {}),
                "status": m.get("status", ""),
            }
            for m in matches
        ]
    }
    
    matches_file = cache_dir / "wc_june_matches.json"
    with open(matches_file, "w", encoding="utf-8") as f:
        json.dump(matches_data, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {matches_file}")
    
    print("\n[2/2] 采集完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
