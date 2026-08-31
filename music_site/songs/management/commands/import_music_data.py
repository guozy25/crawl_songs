import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from songs.models import Song, Artist

class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR).parent
        artists_file = data_dir / "artists_data.json"
        songs_file = data_dir / "songs_data.json"
        if not artists_file.exists():
            print(f"Artists data file not found: {artists_file}")
            return
        if not songs_file.exists():
            print(f"Songs data file not found: {songs_file}")
            return

        with open(artists_file, "r", encoding="utf-8") as file:
            artists_data = json.load(file)

        with open(songs_file, "r", encoding="utf-8") as file:
            songs_data = json.load(file)

        num_artists = 0
        num_songs = 0
        for artist in artists_data:
            artist_id = artist["artist_id"].strip()
            Artist.objects.update_or_create(
                artist_id=artist_id,#查找条件
                defaults={
                    "name": artist["name"].strip(),
                    "img_url": artist["img_url"].strip(),
                    "info": (artist.get("info") or "").strip(),
                }#要更新的内容
            )
            num_artists += 1

        for song in songs_data:
            song_id = song["song_id"].strip()
            artist_id = song["artist_id"].strip()
            artist_obj = Artist.objects.get(artist_id=artist_id)
            Song.objects.update_or_create(
                song_id=song_id,
                defaults={
                    "name": song["song_name"],
                    "photo_url": song["song_photo"],
                    "lyric": song.get("lyric") or [],
                    "artist_name": song["artist_name"],
                    "artist": artist_obj,
                }
            )
            num_songs += 1

        print(f"Imported {num_artists} artists and {num_songs} songs.")
