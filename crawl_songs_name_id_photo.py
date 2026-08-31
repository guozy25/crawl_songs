import requests
import json
import random
import time

"""
没有歌词的歌手：20508，Michita
"""
req_Id = "34db7c10-a395-11f1-bf50-0d4e3c47e2e9"
Secret = "683af2f8796a5c48ac5f97e539c0f37f66b8a1934490f27e62e54febbeef31e802ca9ddd"
cookies = {
        "h5Uuid": "672c04bb759e40a4a1164d4d75580b-9e",
        "Hm_lvt_cdb524f42f0ce19b169a8071123a4797": "1787922050",
        "HMACCOUNT": "88622A3395AD50F5",
        "_ga": "GA1.2.1077267707.1787922125",
        "_gid": "GA1.2.1416875739.1787922125",
        "Hm_lpvt_cdb524f42f0ce19b169a8071123a4797": "1787999423",
        "_ga_ETPBRPM9ML": "GS2.2.s1787997973$o4$g1$t1787999423$j52$l0$h0",
        "Hm_Iuvt_cdb524f42f23cer9b268564v7y735ewrq2324":
            "KjyZhM4crz7trzBRnwPDsjnyke4r8iTd"
    }

with open("artists_data.json", "r", encoding="utf-8") as f:
    artists = json.load(f)

songs = []

count = 0
for i in range(len(artists)):
    artist = artists[i]
    artist_id = artist.get("artist_id")
    url = f"https://www.kuwo.cn/api/www/artist/artistMusic?artistid={artist_id}&pn=1&rn=20&httpsStatus=1&reqId={req_Id}&plat=web_www&from="
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": f"https://www.kuwo.cn/singer_detail/{artist_id}",
        "Secret": f"{Secret}",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 Chrome/152.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        timeout=10
    )
    data = response.json()
    song_name = data['data']['list'][0]['name']
    song_id = data['data']['list'][0]['musicrid']
    song_id = song_id.split("_")[1]
    song_photo = data['data']['list'][0]['pic120']

    songs.append({
        "artist_id": artist_id,
        "artist_name": artist.get("name"),
        "song_name": song_name,
        "song_id": song_id,
        "song_photo": song_photo
        })
    print(i, song_name, song_id, artist.get("name"), artist_id)

    sleep_time = random.uniform(0.1, 1.0)
    time.sleep(sleep_time)
    # count += 1
    # if count < 5:
    #     print(response.status_code)
    #     print(response.text[:500])
#https://www.kuwo.cn/play_detail/228908
with open("songs_data.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=4)
    