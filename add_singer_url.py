import json

with open("artists_data.json", "r", encoding="utf-8") as f:
    artists_data = json.load(f)

for artist in artists_data:
    artist["url"] = f"https://www.kuwo.cn/singer_detail/{artist.get('artist_id')}"

with open("artists_data.json", "w", encoding="utf-8") as f:
    json.dump(artists_data, f, ensure_ascii=False, indent=4)

print("Success")