from django.urls import path
from apps.api.views import ListArtistAPIView, DetailArtistAPIView, \
    ListAlbumAPIView, DetailAlbumAPIView, ListSongAPIView, DetailSongAPIView


urlpatterns = [
    path(
        'artists/', ListArtistAPIView.as_view(), name='artists-list'
    ),
    path(
        'artists/<str:pk>/', DetailArtistAPIView.as_view(), name='artists-detail'
    ),
    path(
        'albums/', ListAlbumAPIView.as_view(), name='albums-list'
    ),
    path(
        'albums/<str:pk>/', DetailAlbumAPIView.as_view(), name='albums-detail'
    ),
    path(
        'songs/', ListSongAPIView.as_view(), name='songs-list'
    ),
    path(
        'songs/<str:pk>/', DetailSongAPIView.as_view(), name='songs-detail'
    ),
]
