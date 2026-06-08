"""
2026世界杯热身赛数据采集 - 扩大版
采集所有已确认ID的球队
"""
import requests
import json
from datetime import datetime
from pathlib import Path

FD_API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
FD_BASE = "https://api.football-data.org/v4"
FD_HEADERS = {"X-Auth-Token": FD_API_KEY}

# 所有已确认的球队 (Football-data ID)
ALL_TEAMS_FD = {
    # 欧洲
    "荷兰": 8601, "法国": 205, "德国": 2001, "意大利": 206,
    "比利时": 196, "葡萄牙": 201, "克罗地亚": 804, "乌克兰": 790,
    "捷克": 798, "奥地利": 816, "匈牙利": 827, "斯洛文尼亚": 777,
    "瑞典": 792, "丹麦": 782, "瑞士": 788,
    "波兰": 24, "罗马尼亚": 774, "塞尔维亚": 14, "斯洛伐克": 773,
    "希腊": 1117, "挪威": 1090, "芬兰": 1099, "冰岛": 18, "苏格兰": 1108,
    # 南美
    "巴西": 764, "阿根廷": 722, "乌拉圭": 21, "哥伦比亚": 818,
    "厄瓜多尔": 791, "巴拉圭": 761,
    # 北美
    "墨西哥": 769, "加拿大": 828,
    # 亚洲
    "沙特阿拉伯": 801, "澳大利亚": 779, "伊朗": 22, "卡塔尔": 1569, "乌兹别克斯坦": 1568,
    # 非洲
    "摩洛哥": 31, "埃及": 32, "尼日利亚": 19, "喀麦隆": 1530,
    "塞内加尔": 13, "加纳": 1504, "科特迪瓦": 1501, "阿尔及利亚": 1532,
}

def get_team_data(name, team_id):
    """获取球队近况"""
    try:
        resp = requests.get(
            f"{FD_BASE}/teams/{team_id}",
            headers=FD_HEADERS, timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            matches = data.get("matches", [])
            
            result = {
                "team": name,
                "api_id": team_id,
                "collected_at": datetime.now().isoformat(),
                "recent_matches": []
            }
            
            for m in matches[:10]:
                match = {
                    "date": m.get("utcDate", "")[:10],
                    "home": m.get("homeTeam", {}).get("name", ""),
                    "away": m.get("awayTeam", {}).get("name", ""),
                    "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
                    "status": m.get("status"),
                    "competition": m.get("competition", {}).get("name", ""),
                }
                result["recent_matches"].append(match)
            
            return result
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
    return None

def main():
    print("=" * 70)
    print("2026世界杯参赛队热身赛数据采集")
    print(f"总计: {len(ALL_TEAMS_FD)} 支球队")
    print("=" * 70)
    
    all_data = {
        "采集时间": datetime.now().isoformat(),
        "总计球队": len(ALL_TEAMS_FD),
        "球队数据": {}
    }
    
    success_count = 0
    
    for name, team_id in ALL_TEAMS_FD.items():
        print(f"采集 {name}...", end=" ", flush=True)
        data = get_team_data(name, team_id)
        if data:
            match_count = len(data["recent_matches"])
            print(f"[OK] {match_count}场")
            all_data["球队数据"][name] = data
            success_count += 1
        else:
            print("[FAIL]")
    
    # 统计
    all_data["成功采集"] = success_count
    
    print(f"\n成功: {success_count}/{len(ALL_TEAMS_FD)}")
    
    # 保存
    output = Path(__file__).parent.parent / "cache" / "wc_teams_full.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存: {output}")
    print("=" * 70)

if __name__ == "__main__":
    main()
