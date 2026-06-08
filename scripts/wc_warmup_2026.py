"""
2026世界杯热身赛数据采集
"""
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

# ===================== 配置 =====================
FD_API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
AF_API_KEY = "270f70b7e6558bd77dc1fa7239fde118"
FD_BASE = "https://api.football-data.org/v4"
AF_BASE = "https://v3.football.api-sports.io"

FD_HEADERS = {"X-Auth-Token": FD_API_KEY}
AF_HEADERS = {"x-apisports-key": AF_API_KEY}

# 2026世界杯参赛队 (部分)
WC_2026_TEAMS = {
    "荷兰": {"fd_id": 8601, "af_id": None},
    "法国": {"fd_id": 205, "af_id": None},
    "德国": {"fd_id": 2001, "af_id": None},
    "巴西": {"fd_id": 764, "af_id": None},
    "阿根廷": {"fd_id": 722, "af_id": None},
}

def get_fd_matches(team_name, fd_id):
    """通过Football-data获取球队近况"""
    try:
        resp = requests.get(
            f"{FD_BASE}/teams/{fd_id}",
            headers=FD_HEADERS, timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            matches = data.get("matches", [])[:10]
            result = {
                "team": team_name,
                "source": "football-data",
                "matches": []
            }
            for m in matches:
                match = {
                    "date": m.get("utcDate", "")[:10],
                    "home": m.get("homeTeam", {}).get("name", ""),
                    "away": m.get("awayTeam", {}).get("name", ""),
                    "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
                    "status": m.get("status"),
                    "competition": m.get("competition", {}).get("name", ""),
                }
                result["matches"].append(match)
            return result
    except Exception as e:
        print(f"  [FD] {team_name} 错误: {e}")
    return None

def get_af_team_fixtures(team_name, af_id):
    """通过API-Football获取球队近况"""
    try:
        resp = requests.get(
            f"{AF_BASE}/fixtures",
            headers=AF_HEADERS,
            params={"team": af_id, "last": 10},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results", 0) > 0:
                result = {
                    "team": team_name,
                    "source": "api-football",
                    "matches": []
                }
                for m in data.get("response", []):
                    fixture = m.get("fixture", {})
                    teams = m.get("teams", {})
                    goals = m.get("goals", {})
                    result["matches"].append({
                        "date": fixture.get("date", "")[:10],
                        "home": teams.get("home", {}).get("name", ""),
                        "away": teams.get("away", {}).get("name", ""),
                        "home_score": goals.get("home"),
                        "away_score": goals.get("away"),
                        "status": fixture.get("status", {}).get("short", ""),
                        "league": m.get("league", {}).get("name", ""),
                    })
                return result
    except Exception as e:
        print(f"  [AF] {team_name} 错误: {e}")
    return None

def main():
    print("=" * 70)
    print("2026世界杯热身赛数据采集")
    print("=" * 70)
    
    all_data = {
        "采集时间": datetime.now().isoformat(),
        "参赛队": {}
    }
    
    # 通过Football-data采集
    print("\n通过Football-data采集...")
    for name, ids in WC_2026_TEAMS.items():
        print(f"  采集 {name}...", end=" ", flush=True)
        data = get_fd_matches(name, ids["fd_id"])
        if data:
            print(f"[OK] {len(data['matches'])}场")
            all_data["参赛队"][name] = data
        else:
            print("[FAIL]")
    
    # 保存
    output = Path(__file__).parent.parent / "cache" / "wc_warmup_latest.json"
    output.parent.mkdir(exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output}")
    print("\n" + "=" * 70)
    print("采集完成!")
    print("=" * 70)

if __name__ == "__main__":
    main()
