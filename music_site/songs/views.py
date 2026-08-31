from django.shortcuts import render, get_object_or_404
from .models import Song
from django.core.paginator import Paginator
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