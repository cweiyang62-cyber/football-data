"""
获取世界杯赔率数据
"""
import requests
import json
from datetime import datetime
from pathlib import Path

ODDS_API_KEY = "6b41102c024582d82e2bdc27bebe54dc"
ODDS_BASE = "https://api.the-odds-api.com/v4"

def get_sports():
    """获取可用赛事列表"""
    url = f"{ODDS_BASE}/sports"
    params = {"apiKey": ODDS_API_KEY}
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"错误: {e}")
    return []

def get_odds(sport_key, regions="eu", markets="h2h"):
    """获取赔率"""
    url = f"{ODDS_BASE}/sports/{sport_key}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": regions,
        "markets": markets,
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"HTTP {resp.status_code}")
    except Exception as e:
        print(f"错误: {e}")
    return []

def main():
    print("=" * 60)
    print("世界杯赔率数据获取")
    print("=" * 60)
    
    # 1. 获取可用赛事
    print("\n[1] 获取可用赛事...")
    sports = get_sports()
    
    # 找足球相关赛事
    soccer_sports = [s for s in sports if "soccer" in s.get("key", "")]
    print(f"找到 {len(soccer_sports)} 个足球赛事:")
    for s in soccer_sports[:10]:
        print(f"  - {s.get('key')}: {s.get('title')}")
    
    # 2. 获取世界杯赔率 (如果可用)
    print("\n[2] 获取世界杯赔率...")
    
    # 尝试不同的世界杯赛事key
    wc_keys = [
        "soccer_world_cup",
        "soccer_fifa_world_cup", 
        "soccer",
        "soccer_international"
    ]
    
    all_odds = []
    for key in wc_keys:
        print(f"\n尝试: {key}")
        odds = get_odds(key)
        if odds:
            print(f"  找到 {len(odds)} 场比赛")
            all_odds.extend(odds)
    
    # 保存结果
    cache_dir = Path(__file__).parent.parent / "cache"
    cache_dir.mkdir(exist_ok=True)
    
    result = {
        "采集时间": datetime.now().isoformat(),
        "比赛数": len(all_odds),
        "赔率数据": []
    }
    
    for match in all_odds[:20]:  # 只保存前20场
        match_info = {
            "id": match.get("id"),
            "sport_key": match.get("sport_key"),
            "commence_time": match.get("commence_time"),
            "home_team": match.get("home_team"),
            "away_team": match.get("away_team"),
            "bookmakers": []
        }
        
        for bm in match.get("bookmakers", [])[:5]:  # 只取前5个博彩公司
            bm_info = {
                "name": bm.get("title"),
                "markets": []
            }
            for mk in bm.get("markets", []):
                if mk.get("key") == "h2h":
                    outcomes = []
                    for oc in mk.get("outcomes", []):
                        outcomes.append({
                            "name": oc.get("name"),
                            "price": oc.get("price")
                        })
                    bm_info["markets"].append({
                        "key": "h2h",
                        "outcomes": outcomes
                    })
            match_info["bookmakers"].append(bm_info)
        
        result["赔率数据"].append(match_info)
    
    output_file = cache_dir / "wc_odds_latest.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到: {output_file}")
    
    # 显示部分结果
    if all_odds:
        print("\n" + "=" * 60)
        print("最新赔率 (前5场)")
        print("=" * 60)
        for match in all_odds[:5]:
            print(f"\n{match.get('home_team')} vs {match.get('away_team')}")
            print(f"时间: {match.get('commence_time', '')[:19]}")
            
            # 显示赔率
            for bm in match.get("bookmakers", [])[:3]:
                print(f"  {bm.get('title')}: ", end="")
                for mk in bm.get("markets", []):
                    if mk.get("key") == "h2h":
                        for oc in mk.get("outcomes", []):
                            print(f"{oc.get('name')}: {oc.get('price')} ", end="")
                        print()
    
    print("\n" + "=" * 60)
    print(f"总计: {len(all_odds)} 场比赛")
    print("=" * 60)

if __name__ == "__main__":
    main()
