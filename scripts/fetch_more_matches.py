"""
获取更多热身赛数据
通过不同联赛和赛事获取
"""
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

FD_API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
FD_BASE = "https://api.football-data.org/v4"
FD_HEADERS = {"X-Auth-Token": FD_API_KEY}

def get_matches_by_competition(comp_code, date_from, date_to):
    """获取特定赛事的比赛"""
    try:
        resp = requests.get(
            f"{FD_BASE}/competitions/{comp_code}/matches",
            headers=FD_HEADERS,
            params={"dateFrom": date_from, "dateTo": date_to},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("matches", [])
    except Exception as e:
        print(f"  错误: {e}")
    return []

def main():
    print("=" * 70)
    print("获取世界杯热身赛数据")
    print("=" * 70)
    
    # 6月1日-6月15日的比赛
    date_from = "2026-06-01"
    date_to = "2026-06-15"
    
    all_matches = []
    
    # 尝试不同赛事
    competitions = {
        "WC": "世界杯预选赛",
        "EC": "欧洲杯",
        "FRIENDLY": "国际友谊赛",
    }
    
    for comp_code, comp_name in competitions.items():
        print(f"\n获取 {comp_name} ({comp_code})...")
        matches = get_matches_by_competition(comp_code, date_from, date_to)
        print(f"  找到 {len(matches)} 场比赛")
        
        for m in matches:
            match_info = {
                "date": m.get("utcDate", "")[:10],
                "time": m.get("utcDate", "")[11:16],
                "home": m.get("homeTeam", {}).get("name", ""),
                "away": m.get("awayTeam", {}).get("name", ""),
                "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
                "status": m.get("status", ""),
                "competition": m.get("competition", {}).get("name", ""),
            }
            all_matches.append(match_info)
    
    # 按日期排序
    all_matches.sort(key=lambda x: x.get("date", ""))
    
    print(f"\n总计获取 {len(all_matches)} 场比赛")
    
    # 显示所有比赛
    print("\n" + "=" * 70)
    print("完整赛程")
    print("=" * 70)
    
    current_date = ""
    for m in all_matches:
        date = m.get("date", "")
        if date != current_date:
            current_date = date
            print(f"\n[DATE] {date}")
        
        status_icon = "[FIN]" if m["status"] == "FINISHED" else "[SCH]"
        if m["status"] == "FINISHED":
            score = f"{m['home_score']}:{m['away_score']}"
            print(f"  {status_icon} {m['home']} vs {m['away']} [{score}]")
        else:
            time = m.get("time", "")
            print(f"  {status_icon} {m['home']} vs {m['away']} [{time}]")
    
    # 保存
    output = Path(__file__).parent.parent / "cache" / "wc_june_matches.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump({
            "采集时间": datetime.now().isoformat(),
            "比赛数": len(all_matches),
            "比赛": all_matches
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存: {output}")

if __name__ == "__main__":
    main()
