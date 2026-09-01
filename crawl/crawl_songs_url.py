import json

with open("songs_data.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

#https://www.kuwo.cn/play_detail/228908
for song in songs:
    song_id = song.get("song_id")
    url = f"https://www.kuwo.cn/play_detail/{song_id}"
    songs[songs.index(song)]["url"] = url

with open("songs_data.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=4)

