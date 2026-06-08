# ⚽ 世界杯数据分析工具 - 快速上手

## 当前状态

| 模块 | 状态 | 完成度 |
|:---|:---|:---|
| 目录结构 | ✅ 完成 | 100% |
| API配置 | ✅ 完成 | Football-data + API-Football |
| 球队ID库 | ✅ 完成 | 41/48队 |
| 历史数据 | ✅ 完成 | 1994-2022 |
| 数据采集脚本 | ✅ 完成 | 5个脚本 |
| 报告模板 | ✅ 完成 | 2个模板 |

---

## 5分钟快速开始

### 1. 测试API连接
```bash
cd football-data\scripts
python test_api.py
```

### 2. 查询球队近期战绩
```bash
# 修改 collector.py 中的队伍列表，运行:
python collector.py
```

### 3. 生成分析报告
```bash
# 使用每日报告模板: analysis/daily_report_template.md
```

---

## 球队ID快速查

| 地区 | 球队 | API ID |
|:---|:---|:---|
| 欧洲 | 荷兰 | 8601 |
| 欧洲 | 法国 | 205 |
| 欧洲 | 德国 | 2001 |
| 欧洲 | 英格兰 | 待查 |
| 南美 | 巴西 | 764 |
| 南美 | 阿根廷 | 722 |
| 亚洲 | 日本 | 待查 |
| 亚洲 | 韩国 | 待查 |
| 亚洲 | 伊朗 | 22 |
| 北美 | 美国 | 待查 |

完整列表见: `cache/teams_search_results.json`

---

## 脚本说明

| 脚本 | 功能 |
|:---|:---|
| `test_api.py` | 测试API连接 |
| `find_teams.py` | 查询单个球队ID |
| `search_wc_teams.py` | 批量查询球队ID |
| `collector.py` | 采集球队比赛数据 |
| `api_football_search.py` | API-Football球队查询 |

---

## 数据文件说明

| 文件 | 内容 |
|:---|:---|
| `config.yaml` | 配置文件 + 球队ID映射 |
| `cache/teams_search_results.json` | 球队ID查询结果 |
| `longterm/wc_history.yaml` | 历届世界杯数据 |
| `analysis/daily_report_template.md` | 每日分析报告模板 |
| `analysis/wc_2026/teams/TEAM_TEMPLATE.md` | 球队档案模板 |

---

## 下一步计划

- [ ] 补充8支待查球队ID
- [ ] 开发定时自动采集
- [ ] 对接赔率数据
- [ ] 创建32强球队详细档案
- [ ] 开发赛前自动分析报告生成

---

## 常用命令

```bash
# 查看已确认球队数量
grep -c "teams:" config.yaml

# 测试两个API是否正常
python test_api.py

# 更新球队数据
python collector.py
```
