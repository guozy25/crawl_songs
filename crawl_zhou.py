import requests
import json

# 先请求一次首页，获取 kw_token 放入 Cookie
Secret = "683af2f8796a5c48ac5f97e539c0f37f66b8a1934490f27e62e54febbeef31e802ca9ddd"
session = requests.Session()
home_url = "https://www.kuwo.cn/singer_detail/336"
home_headers = {
    "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": f"https://www.kuwo.cn/singer_detail/336",
            "Secret": f"{Secret}",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/152.0.0.0 Safari/537.36"
            )
            }
resp = session.get(home_url, headers=home_headers)
# 从 session.cookies 中提取 kw_token
kw_token = session.cookies.get("kw_token", "")
print("kw_token:", kw_token)

# 构造 API 请求
api_url = "https://www.kuwo.cn/api/www/artist/artistMusic"
params = {
    "artistid": "336",
    "pn": "1",
    "rn": "20",
    "httpsStatus": "1",
    "plat": "web_www",
    "from": ""
}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.kuwo.cn/singer_detail/336",
    "csrf": kw_token,          # 关键字段
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": "; ".join([f"{c.name}={c.value}" for c in session.cookies])
}

response = session.get(api_url, params=params, headers=headers)
print(response.status_code)
data = response.json()
print(data)