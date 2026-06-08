"""
最后8队ID查询
通过多种渠道尝试
"""
import requests
import time

FD_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
AF_KEY = "270f70b7e6558bd77dc1fa7239fde118"
FD_BASE = "https://api.football-data.org/v4"
AF_BASE = "https://v3.football.api-sports.io"

FD_HEADERS = {"X-Auth-Token": FD_KEY}
AF_HEADERS = {"x-apisports-key": AF_KEY}

# 剩余8队 + 多种搜索词
remaining_teams = {
    "Wales": ["Wales", "Welsh"],
    "Ireland": ["Ireland", "Republic of Ireland", "Irish"],
    "Peru": ["Peru", "Peruvian"],
    "Chile": ["Chile", "Chilean"],
    "Venezuela": ["Venezuela", "Venezuelan"],
    "Japan": ["Japan", "Japanese"],
    "Korea": ["Korea", "Korean", "South Korea", "Korea Republic"],
    "USA": ["USA", "United States", "United States of America", "American"],
}

def search_fd_all(name):
    """搜索Football-data所有赛事"""
    leagues = [
        ("WC", "FIFA World Cup"),
        ("EC", "European Championship"),
        ("CL", "Champions League"),
        ("EL", "Europa League"),
        ("BL1", "Bundesliga"),
        ("PL", "Premier League"),
        ("PD", "La Liga"),
        ("SA", "Serie A"),
        ("FL1", "Ligue 1"),
        ("DED", "Eredivisie"),
        ("PPL", "Primeira Liga"),
        ("BSA", "Brasileirao"),
        ("MLS", "MLS"),  # 可能没有
    ]
    
    for code, name_league in leagues:
        try:
            resp = requests.get(
                f"{FD_BASE}/competitions/{code}/teams",
                headers=FD_HEADERS, timeout=10
            )
            if resp.status_code == 200:
                for team in resp.json().get("teams", []):
                    if name.lower() in team.get("name", "").lower():
                        return team["id"], team["name"], "FD", code
        except:
            pass
    return None

def search_af(name):
    """搜索API-Football"""
    for search_name in name:
        try:
            resp = requests.get(
                f"{AF_BASE}/teams",
                headers=AF_HEADERS,
                params={"name": search_name, "league": 1, "season": 2024},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results", 0) > 0:
                    team = data["response"][0]["team"]
                    return team["id"], team["name"], "AF"
        except:
            pass
    return None

def main():
    print("=" * 60)
    print("查找最后8队ID")
    print("=" * 60)
    
    results = {}
    
    for orig_name, search_names in remaining_teams.items():
        print(f"\n查找: {orig_name}")
        
        # 先试API-Football
        print(f"  [AF] 尝试...", end=" ", flush=True)
        result = search_af(search_names)
        if result:
            print(f"[OK] ID={result[0]} ({result[1]})")
            results[orig_name] = {"id": result[0], "name": result[1], "source": result[2]}
            continue
        
        # 再试Football-data
        for search_name in search_names:
            print(f"  [FD] {search_name}...", end=" ", flush=True)
            result = search_fd_all(search_name)
            if result:
                print(f"[OK] ID={result[0]} ({result[1]})")
                results[orig_name] = {"id": result[0], "name": result[1], "source": result[2]}
                break
            else:
                print("[X]")
        
        if orig_name not in results:
            print(f"  [FAIL] 未找到")
        
        time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print("结果汇总:")
    print("=" * 60)
    for name, data in results.items():
        print(f'  "{name}": {data["id"]},  # {data["name"]} ({data["source"]})')

if __name__ == "__main__":
    main()
