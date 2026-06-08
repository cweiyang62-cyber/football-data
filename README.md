# 🏆 世界杯数据分析工具

备战2026世界杯数据采集与分析框架

---

## 当前完成状态

| 模块 | 状态 | 说明 |
|:---|:---|:---|
| ✅ 目录结构 | 完成 | scripts/cache/longterm/analysis |
| ✅ API配置 | 完成 | Football-data + API-Football双源 |
| ✅ 球队ID库 | 完成 | 47/48队已确认 |
| ✅ 历史数据 | 完成 | 1994-2022完整录入 |
| ✅ 采集脚本 | 完成 | 10个Python脚本 |
| ✅ 报告模板 | 完成 | 每日报告+球队档案 |
| ✅ GitHub Actions | 完成 | 可自动定时采集 |

---

## 目录结构

```
football-data/
├── config.yaml              # 配置文件 + 球队ID映射(47队)
├── README.md               # 本文件
├── GITHUB_SETUP.md         # GitHub Actions 设置指南
├── requirements.txt        # Python依赖
│
├── .github/
│   └── workflows/
│       └── collect.yml     # 自动采集workflow
│
├── scripts/                 # 数据采集脚本
│   ├── github_collect.py  # GitHub Actions专用
│   ├── show_matches.py    # 获取热身赛
│   ├── wc_warmup_full.py  # 球队数据采集
│   └── ...
│
├── cache/                   # 缓存数据 (git同步)
│   └── wc_june_matches.json
│
├── longterm/                # 长期存储
│   └── wc_history.yaml     # 历届世界杯数据
│
└── analysis/                # 分析输出
    └── wc_2026_warmup_report.md
```

---

## 快速开始

### 本地运行
```bash
cd scripts
python github_collect.py        # 采集热身赛
python show_matches.py         # 显示比赛
```

### GitHub Actions 自动采集
详见 `GITHUB_SETUP.md`

---

## 已确认球队ID (47队)

### 欧洲 (27队)
荷兰、法国、德国、意大利、比利时、葡萄牙、克罗地亚、乌克兰、捷克、奥地利、匈牙利、斯洛文尼亚、瑞典、丹麦、瑞士、波兰、罗马尼亚、塞尔维亚、斯洛伐克、希腊、土耳其、挪威、芬兰、冰岛、苏格兰、威尔士、爱尔兰

### 南美 (9队)
巴西、阿根廷、乌拉圭、哥伦比亚、厄瓜多尔、巴拉圭、秘鲁、智利、委内瑞拉

### 北美 (3队)
墨西哥、加拿大、美国

### 亚洲 (6队)
沙特阿拉伯、澳大利亚、伊朗、卡塔尔、乌兹别克斯坦、日本

### 非洲 (8队)
摩洛哥、埃及、尼日利亚、喀麦隆、塞内加尔、加纳、科特迪瓦、阿尔及利亚

### 待查
韩国 (API限速)

---

## 历届世界杯数据

已录入: 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022

---

## 待办事项

- [x] GitHub Actions 自动采集配置
- [ ] 补充韩国ID
- [ ] 创建32强球队详细档案
- [ ] 对接赔率数据
