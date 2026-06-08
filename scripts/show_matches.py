"""
获取热身赛数据 - 纯文件输出
"""
import requests
import json
from datetime import datetime
from pathlib import Path

FD_API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
FD_BASE = "https://api.football-data.org/v4"
FD_HEADERS = {"X-Auth-Token": FD_API_KEY}

def get_matches(comp_code, date_from, date_to):
    try:
        resp = requests.get(
            f"{FD_BASE}/competitions/{comp_code}/matches",
            headers=FD_HEADERS,
            params={"dateFrom": date_from, "dateTo": date_to},
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json().get("matches", [])
    except:
        pass
    return []

def main():
    matches = get_matches("WC", "2026-06-01", "2026-06-20")
    
    result = []
    for m in matches:
        result.append({
            "date": m.get("utcDate", "")[:10],
            "time": m.get("utcDate", "")[11:16],
            "home": m.get("homeTeam", {}).get("name", ""),
            "away": m.get("awayTeam", {}).get("name", ""),
            "score": m.get("score", {}).get("fullTime", {}),
            "status": m.get("status", ""),
            "competition": m.get("competition", {}).get("name", ""),
        })
    
    result.sort(key=lambda x: x.get("date", ""))
    
    # 保存
    output = Path(__file__).parent.parent / "cache" / "wc_june_matches.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump({
            "采集时间": datetime.now().isoformat(),
            "总计": len(result),
            "比赛": result
        }, f, ensure_ascii=False, indent=2)
    
    print(f"找到 {len(result)} 场比赛，已保存到: {output}")
    
    # 简单显示
    for m in result:
        score_str = ""
        if m["status"] == "FINISHED":
            s = m["score"]
            score_str = f"{s.get('home')}:{s.get('away')}"
        else:
            score_str = m["time"]
        print(f"{m['date']} | {m['home']} vs {m['away']} | {score_str}")

if __name__ == "__main__":
    main()
