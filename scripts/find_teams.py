"""
根据队名搜索球队ID
"""
import requests
import json

API_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
BASE_URL = "https://api.football-data.org/v4"

def search_team(keyword):
    """搜索包含关键词的球队"""
    headers = {"X-Auth-Token": API_KEY}
    
    # 尝试从各联赛搜索
    leagues = {
        "EC": "UEFA European Championship",
        "WC": "FIFA World Cup", 
        "CL": "UEFA Champions League",
        "PL": "Premier League",
        "BL1": "Bundesliga",
        "PD": "La Liga",
        "SA": "Serie A",
        "FL1": "Ligue 1"
    }
    
    print(f"\n搜索关键词: {keyword}")
    print("-" * 50)
    
    found = []
    
    for code, name in leagues.items():
        try:
            resp = requests.get(
                f"{BASE_URL}/competitions/{code}/teams",
                headers=headers,
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                for team in data.get("teams", []):
                    if keyword.lower() in team.get("name", "").lower():
                        found.append({
                            "name": team.get("name"),
                            "tla": team.get("tla"),
                            "id": team.get("id"),
                            "league": name
                        })
        except:
            pass
    
    # 显示结果
    if found:
        print(f"找到 {len(found)} 个结果:")
        for t in found:
            print(f"  [{t['id']}] {t['name']} ({t['tla']}) - {t['league']}")
    else:
        print("未找到匹配的球队")
    
    return found

def get_team_by_id(team_id):
    """根据ID获取球队详情"""
    headers = {"X-Auth-Token": API_KEY}
    
    try:
        resp = requests.get(f"{BASE_URL}/teams/{team_id}", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print(f"\n球队ID: {data.get('id')}")
        print(f"名称: {data.get('name')}")
        print(f"简称: {data.get('tla')}")
        print(f"队徽: {data.get('crest', 'N/A')}")
        return data
    except Exception as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        search_team(keyword)
    else:
        print("用法: python find_teams.py <球队关键词>")
        print("\n示例:")
        print("  python find_teams.py Netherlands")
        print("  python find_teams.py France")
        print("  python find_teams.py Brazil")
        print("\n或者直接查询ID:")
        print("  python find_teams.py --id 195")
