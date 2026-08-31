from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    img_url = models.URLField(max_length=200)
    info = models.TextField(blank=True, default = "")

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'
        ordering = ["name"]


class Song(models.Model):
    song_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    photo_url = models.URLField(max_length=200)
    lyric = models.JSONField()
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='songs')

    class Meta:
        ordering = ["id"]
        verbose_name = "歌曲"
        verbose_name_plural = "歌曲"
        