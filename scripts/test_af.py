"""
测试 API-Football 直接连接
"""
import requests

API_KEY = "270f70b7e6558bd77dc1fa7239fde118"

headers = {"x-apisports-key": API_KEY}

# 试几个不同端点
endpoints = [
    ("https://v3.api-football.com/status", None),
    ("https://v3.api-football.com/timezone", None),
    ("https://api-football.com/v3/status", None),
]

print("测试不同端点...")
for url, params in endpoints:
    print(f"\n尝试: {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"  状态: {resp.status_code}")
        print(f"  内容: {resp.text[:200]}")
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
