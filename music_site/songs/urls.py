from django.urls import path

from . import views

app_name = "songs"

urlpatterns = [path("", views.song_list, name="song_list"),
               path("songs/<str:song_id>/", views.song_detail, name="song_detail"),
               path("artists/", views.singer_list, name="artists"),
               path("artists/<str:artist_id>/", views.artist_detail, name="artist_detail"),
               path("search/", views.search_view,name="search"),
            ]