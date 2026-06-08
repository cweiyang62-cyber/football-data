"""
世界杯备战数据采集主脚本
功能:
  1. 采集热身赛数据
  2. 采集参赛队近期战绩
  3. 采集赔率数据
  4. 存储到本地
"""
import requests
import json
import os
import yaml
from datetime import datetime, timedelta
from pathlib import Path

# ===================== 配置 =====================
API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"
CACHE_DIR = Path(__file__).parent.parent / "cache"
LONGTERM_DIR = Path(__file__).parent.parent / "longterm"

HEADERS = {"X-Auth-Token": API_KEY}

# 2026世界杯相关球队ID映射 (Football-data API的team id)
WC_2026_TEAMS = {
    "荷兰": 195,
    "法国": 197,
    "德国": 200,
    "英格兰": 197,  # 待确认
    "西班牙": 198,
    "意大利": 200,  # 待确认
    "比利时": 196,
    "葡萄牙": 201,
    "巴西": 204,
    "阿根廷": 207,
}

# ===================== 工具函数 =====================
def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_json(data, filepath):
    """保存JSON数据"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath):
    """加载JSON数据"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def api_get(endpoint, params=None):
    """通用的API请求"""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

# ===================== 采集函数 =====================
def collect_team_matches(team_name, days=30):
    """
    采集指定球队近期的比赛数据
    days: 回溯天数
    """
    team_id = WC_2026_TEAMS.get(team_name)
    if not team_id:
        print(f"⚠️ 未知球队: {team_name}")
        return None
    
    print(f"\n📊 采集: {team_name} (ID: {team_id})")
    
    try:
        # 获取球队详情和赛程
        data = api_get(f"teams/{team_id}")
        
        # 获取未来比赛
        matches = data.get("matches", [])
        
        result = {
            "team": team_name,
            "team_id": team_id,
            "collected_at": datetime.now().isoformat(),
            "matches": []
        }
        
        for m in matches[:10]:  # 最近10场
            match_info = {
                "id": m.get("id"),
                "home_team": m.get("homeTeam", {}).get("name"),
                "away_team": m.get("awayTeam", {}).get("name"),
                "date": m.get("utcDate"),
                "status": m.get("status"),
                "score": m.get("score", {}).get("fullTime"),
                "competition": m.get("competition", {}).get("name"),
            }
            result["matches"].append(match_info)
            
        print(f"   ✅ 获取 {len(result['matches'])} 场比赛")
        return result
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None

def collect_competition_matches(competition_code="WC", days=90):
    """
    采集特定赛事的比赛数据
    competition_code: 赛事代码 (WC=世界杯, EC=欧洲杯等)
    """
    print(f"\n📊 采集赛事: {competition_code}")
    
    try:
        # 获取赛事信息
        comp = api_get(f"competitions/{competition_code}")
        print(f"   赛事: {comp.get('name')}")
        
        # 获取赛程
        today = datetime.now()
        end_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")
        start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        
        matches = api_get(
            f"competitions/{competition_code}/matches",
            params={
                "dateFrom": start_date,
                "dateTo": end_date,
                "status": "FINISHED,SCHEDULED"
            }
        )
        
        result = {
            "competition": comp.get("name"),
            "code": competition_code,
            "collected_at": datetime.now().isoformat(),
            "matches": []
        }
        
        for m in matches.get("matches", []):
            match_info = {
                "id": m.get("id"),
                "home_team": m.get("homeTeam", {}).get("name"),
                "away_team": m.get("awayTeam", {}).get("name"),
                "date": m.get("utcDate"),
                "status": m.get("status"),
                "score": m.get("score", {}).get("fullTime"),
            }
            result["matches"].append(match_info)
        
        print(f"   ✅ 获取 {len(result['matches'])} 场比赛")
        return result
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None

def collect_all_wc_teams():
    """
    采集所有世界杯参赛队数据
    """
    print("\n" + "=" * 60)
    print("🌍 开始采集2026世界杯参赛队数据")
    print("=" * 60)
    
    all_data = {
        "collected_at": datetime.now().isoformat(),
        "teams": []
    }
    
    for team_name in WC_2026_TEAMS.keys():
        team_data = collect_team_matches(team_name, days=30)
        if team_data:
            all_data["teams"].append(team_data)
    
    # 保存
    output_path = CACHE_DIR / "wc_2026_teams_latest.json"
    save_json(all_data, output_path)
    print(f"\n💾 已保存到: {output_path}")
    
    return all_data

# ===================== 主程序 =====================
def main():
    print("\n" + "=" * 60)
    print("⚽ 世界杯数据采集工具 v1.0")
    print("=" * 60)
    
    # 确保目录存在
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 采集所有世界杯参赛队数据
    data = collect_all_wc_teams()
    
    print("\n" + "=" * 60)
    print("✅ 采集完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
