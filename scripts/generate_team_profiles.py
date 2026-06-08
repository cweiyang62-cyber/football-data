"""
批量生成32强球队档案
"""
import requests
import json
from pathlib import Path
from datetime import datetime

FD_KEY = "c50e3649bded4ee09620aaf8c820a8ac"
FD_BASE = "https://api.football-data.org/v4"
FD_HEADERS = {"X-Auth-Token": FD_KEY}

# 32强球队 (按分组)
WC_2026_TEAMS = {
    "荷兰": {"tla": "NED", "id": 8601, "分组": "A", "founded": 1889, " stadium": "约翰·克鲁伊夫竞技场"},
    "卡塔尔": {"tla": "QAT", "id": 1569, "分组": "A", "founded": 1957, "stadium": "卢塞尔体育场"},
    "厄瓜多尔": {"tla": "ECU", "id": 791, "分组": "A", "founded": 1924, "stadium": " Estadio Rodrigo Paz"},
    "塞内加尔": {"tla": "SEN", "id": 13, "分组": "A", "founded": 1960, "stadium": "Stade de la Paix"},
    
    "英格兰": {"tla": "ENG", "id": 205, "分组": "B", "founded": 1863, "stadium": "温布利球场"},
    "伊朗": {"tla": "IRN", "id": 22, "分组": "B", "founded": 1920, "stadium": "阿扎迪体育场"},
    "美国": {"tla": "USA", "id": 2384, "分组": "B", "founded": 1913, "stadium": "大通体育场"},
    "威尔士": {"tla": "WAL", "id": 767, "分组": "B", "founded": 1876, "stadium": "千禧球场"},
    
    "阿根廷": {"tla": "ARG", "id": 722, "分组": "C", "founded": 1893, "stadium": "纪念碑球场"},
    "沙特阿拉伯": {"tla": "KSA", "id": 801, "分组": "C", "founded": 1956, "stadium": "法赫德国王国际体育场"},
    "墨西哥": {"tla": "MEX", "id": 769, "分组": "C", "founded": 1927, "stadium": "阿兹特克体育场"},
    "波兰": {"tla": "POL", "id": 24, "分组": "C", "founded": 1919, "stadium": "国家体育场"},
    
    "法国": {"tla": "FRA", "id": 205, "分组": "D", "founded": 1919, "stadium": "法兰西体育场"},
    "澳大利亚": {"tla": "AUS", "id": 779, "分组": "D", "founded": 1963, "stadium": "墨尔本 Rectangular Stadium"},
    "丹麦": {"tla": "DEN", "id": 782, "分组": "D", "founded": 1889, "stadium": "帕肯球场"},
    "突尼斯": {"tla": "TUN", "id": 1530, "分组": "D", "founded": 1956, "stadium": "哈比卜·布尔吉巴体育场"},
    
    "西班牙": {"tla": "ESP", "id": 198, "分组": "E", "founded": 1909, "stadium": "万达大都会体育场"},
    "德国": {"tla": "GER", "id": 2001, "分组": "E", "founded": 1900, "stadium": "安联竞技场"},
    "日本": {"tla": "JPN", "id": 12, "分组": "E", "founded": 1921, "stadium": "日本国立竞技场"},
    "哥斯达黎加": {"tla": "CRC", "id": None, "分组": "E", "founded": 1921, "stadium": " Estadio Nacional"},
    
    "比利时": {"tla": "BEL", "id": 196, "分组": "F", "founded": 1895, "stadium": "博杜安国王体育场"},
    "加拿大": {"tla": "CAN", "id": 828, "分组": "F", "founded": 1904, "stadium": "BMO Field"},
    "摩洛哥": {"tla": "MAR", "id": 31, "分组": "F", "founded": 1956, "stadium": "穆罕默德五世体育场"},
    "克罗地亚": {"tla": "CRO", "id": 804, "分组": "F", "founded": 1912, "stadium": "萨格勒布体育场"},
    
    "巴西": {"tla": "BRA", "id": 764, "分组": "G", "founded": 1914, "stadium": "马拉卡纳体育场"},
    "塞尔维亚": {"tla": "SRB", "id": 14, "分组": "G", "founded": 1919, "stadium": "Rajko Mitić Stadium"},
    "瑞士": {"tla": "SUI", "id": 788, "分组": "G", "founded": 1898, "stadium": "Stade de Suisse"},
    "喀麦隆": {"tla": "CMR", "id": 1530, "分组": "G", "founded": 1957, "stadium": "Stade d'Olembe"},
    
    "葡萄牙": {"tla": "POR", "id": 201, "分组": "H", "founded": 1914, "stadium": "光明体育场"},
    "加纳": {"tla": "GHA", "id": 1504, "分组": "H", "founded": 1920, "stadium": "阿克拉体育场"},
    "乌拉圭": {"tla": "URU", "id": 21, "分组": "H", "founded": 1900, "stadium": "Centenario体育场"},
    "韩国": {"tla": "KOR", "id": None, "分组": "H", "founded": 1948, "stadium": "首尔世界杯体育场"},
}

def get_team_recent_matches(team_id):
    """获取球队近期战绩"""
    if not team_id:
        return []
    try:
        resp = requests.get(
            f"{FD_BASE}/teams/{team_id}/matches",
            headers=FD_HEADERS,
            params={"status": "FINISHED", "limit": 10},
            timeout=10
        )
        if resp.status_code == 200:
            matches = resp.json().get("matches", [])
            return [
                {
                    "date": m.get("utcDate", "")[:10],
                    "home": m.get("homeTeam", {}).get("name", ""),
                    "away": m.get("awayTeam", {}).get("name", ""),
                    "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
                    "competition": m.get("competition", {}).get("name", ""),
                }
                for m in matches
            ]
    except:
        pass
    return []

def generate_profile(name, info, matches):
    """生成球队档案"""
    # 计算近期战绩统计
    wins, draws, losses = 0, 0, 0
    goals_for, goals_against = 0, 0
    
    for m in matches:
        if m.get("home") == name:
            score = m.get("home_score")
            opp_score = m.get("away_score")
        else:
            score = m.get("away_score")
            opp_score = m.get("home_score")
        
        if score is not None and opp_score is not None:
            goals_for += score
            goals_against += opp_score
            if score > opp_score:
                wins += 1
            elif score == opp_score:
                draws += 1
            else:
                losses += 1
    
    total = wins + draws + losses
    record = f"{wins}胜{draws}平{losses}负" if total > 0 else "数据待查"
    avg_gf = f"{goals_for/total:.1f}" if total > 0 else "?"
    avg_ga = f"{goals_against/total:.1f}" if total > 0 else "?"
    
    # 格式化近期战绩表格
    recent_matches = ""
    for m in matches[:5]:
        date = m.get("date", "")
        home = m.get("home", "")
        away = m.get("away", "")
        hs = m.get("home_score")
        as_ = m.get("away_score")
        
        if hs is not None and as_ is not None:
            score_str = f"{hs}:{as_}"
            if home == name:
                result = "胜" if hs > as_ else ("平" if hs == as_ else "负")
                opponent = away
                score_str = f"{hs}:{as_}"
            else:
                result = "胜" if as_ > hs else ("平" if as_ == hs else "负")
                opponent = home
                score_str = f"{as_}:{hs}"
        else:
            result = "?"
            opponent = home if away == name else away
            score_str = "?"
        
        recent_matches += f"| {date} | {opponent} | {score_str} | {result} |\n"
    
    if not recent_matches:
        recent_matches = "| 数据待查 | - | - | - |\n"
    
    # 生成档案内容
    profile = f"""# {name} 国家足球队

**FIFA排名**: 待更新  
**分组**: {info['分组']}组  
**成立年份**: {info['founded']}  
**主场**: {info.get('stadium', '待定')}  

---

## 基本信息

| 项目 | 数据 |
|:---|:---|
| 队名 | {name} |
| 简称 | {info['tla']} |
| 成立 | {info['founded']} |
| 主场 | {info.get('stadium', '待定')} |

---

## 近期战绩 (近10场)

| 日期 | 对手 | 比分 | 结果 |
|:---|:---|:---|:---|
{recent_matches}

**总计**: {record} | **场均进球**: {avg_gf} | **场均失球**: {avg_ga}

---

## 进攻数据

| 指标 | 数值 |
|:---|:---|
| 场均进球 | {avg_gf} |
| 进球效率 | {'待统计' if total == 0 else '正常'} |

---

## 防守数据

| 指标 | 数值 |
|:---|:---|
| 场均失球 | {avg_ga} |
| 零封率 | {'待统计' if total == 0 else '待统计'} |

---

## 2026世界杯前景

**分组**: {info['分组']}组

**优势**:
- 待分析
- 主场/备战情况待更新

**劣势**:
- 待分析

**预测**: 小组赛阶段

---

*档案生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*数据来源: Football-data API*
"""
    
    return profile

def main():
    teams_dir = Path(__file__).parent.parent / "analysis" / "wc_2026" / "teams"
    teams_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("批量生成32强球队档案")
    print("=" * 60)
    
    generated = 0
    
    for name, info in WC_2026_TEAMS.items():
        team_id = info.get("id")
        print(f"处理 {name}...", end=" ", flush=True)
        
        # 获取近期战绩
        matches = get_team_recent_matches(team_id)
        
        # 生成档案
        profile = generate_profile(name, info, matches)
        
        # 保存
        filename = f"{info['tla']}_{name}.md"
        filepath = teams_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(profile)
        
        print(f"[OK] {len(matches)}场")
        generated += 1
    
    print(f"\n完成! 生成 {generated} 个球队档案")
    print(f"保存位置: {teams_dir}")

if __name__ == "__main__":
    main()
