from django.shortcuts import render, get_object_or_404
from .models import Song, Artist
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
import time
# Create your views here.

def song_list(request):
    song_queryset = Song.objects.select_related("artist").all()
    paginator = Paginator(song_queryset, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'songs/song_list.html', {'page_obj': page_obj})

def song_detail(request, song_id):
    song = get_object_or_404(Song.objects.select_related("artist"), song_id=song_id)
    return render(request, 'songs/song_detail.html', {'song': song})

def singer_list(request):
    singer_queryset = Artist.objects.annotate(song_count=Count("songs"))
    paginator = Paginator(singer_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'songs/artist_list.html', {'page_obj': page_obj})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, artist_id=artist_id)
    songs = Song.objects.filter(artist=artist).select_related("artist")
    paginator = Paginator(songs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'songs/artist_detail.html',
        {'artist': artist, 'page_obj': page_obj}
    )

def search_view(request):
    keyword = request.GET.get("q", "").strip()
    search_type = request.GET.get("type", "song")

    if search_type not in ["song", "artist"]:
        search_type = "song"

    start_time = time.perf_counter()

    if search_type == "song":
        queryset = Song.objects.select_related("artist").filter(
            name__icontains=keyword
        )
    else:
        queryset = Artist.objects.filter(
            name__icontains=keyword
        )

    paginator = Paginator(queryset, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    page_obj.object_list = list(page_obj.object_list)
    end_time = time.perf_counter()
    search_time = (end_time - start_time) * 1000

    return render(
        request,
        "songs/search.html",
        {
            "keyword": keyword,
            "search_type": search_type,
            "page_obj": page_obj,
            "search_time": f"{search_time:.2f}",
        }
    )
