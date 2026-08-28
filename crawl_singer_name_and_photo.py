import requests
from bs4 import BeautifulSoup
import json
import re

head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.5.2 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        }
urls = ['https://m.kuwo.cn/newh5/artist/artistList?id=1', 
        'http://m.kuwo.cn/newh5/artist/artistList?id=2', 
        'http://m.kuwo.cn/newh5/artist/artistList?id=4',
        'http://m.kuwo.cn/newh5/artist/artistList?id=5' ]
artists_data = []
for i in range(len(urls)):
    url = urls[i]
    r = requests.get(url, headers=head, timeout=10)
    if r.status_code == requests.codes.ok:
        data = r.text

    soup = BeautifulSoup(data, 'html.parser')
    """
    <li class="singBox_special clearfix" onclick="jumpArtistDetail('983',event)">
        <div class="specialImgBox fl">
            <img src="https://star.kuwo.cn/star/starheads/120/s4s24/98/3925627773.png">
        </div>
        <div class="Sp_singTex fl">
            <div class="Sp_singTexUp fl">
                <p class="artistName">方大同</p>
                <p class="singCount">549首歌</p>
            </div>
            <a class="artist_toright at2 fr"></a>
        </div>
    </li>
    """
    
    items = soup.find_all("li", class_="singBox_special")

    for item in items:
        name = item.find("p", class_="artistName").get_text()

        img = item.find("img")
        img_url = img.get("src")

        onclick_attr = item.get("onclick")
        match = re.search(r"jumpArtistDetail\('(\d+)'", onclick_attr)
        artist_id = match.group(1)

        artists_data.append({
            "name": name,
            "img_url": img_url,
            "artist_id": artist_id
        })

output_file = "artists_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(artists_data, f, ensure_ascii=False)

print(f"{len(artists_data)} 位歌手数据，存入 {output_file}\n")