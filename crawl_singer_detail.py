from bs4 import BeautifulSoup
import requests
import json

head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.5.2 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        "Referer": "https://www.example.com/"
        }

with open("artists_data.json", "r", encoding="utf-8") as f:
    artists_data = json.load(f)

artist_ids = [artist.get("artist_id") for artist in artists_data]

#for artist_id in artist_ids:
url = f"https://www.kuwo.cn/singer_detail/336/info"
r = requests.get(url, headers = head, timeout = 1)
if r.status_code == requests.codes.ok:
    data = r.text
else: 
    print(f"请求失败，状态码：{r.status_code}")

data = BeautifulSoup(data, 'html.parser')
info = data.find("p", class_="info").get_text()
print(info)

