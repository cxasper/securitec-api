from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from apps.api.views import ListArtistAPIView, DetailArtistAPIView, \
    ListAlbumAPIView, DetailAlbumAPIView, ListSongAPIView, DetailSongAPIView, \
    ListCountryAPIView, SongsByAlbumAPIView, SongsByArtistAPIView, \
    AlbumsByArtistAPIView


urlpatterns = [
    path(r'login/', obtain_auth_token, name='login'),
    path(
        'countries/', ListCountryAPIView.as_view(), name='countries-list'
    ),
    path(
        'artists/<str:artist>/albums/', AlbumsByArtistAPIView.as_view()
    ),
    path(
        'artists/<str:artist>/songs/', SongsByArtistAPIView.as_view()
    ),
    path(
        'artists/', ListArtistAPIView.as_view(), name='artists-list'
    ),
    path(
        'artists/<str:pk>/', DetailArtistAPIView.as_view(), name='artists-detail'
    ),
    path(
        'albums/<str:album>/songs/', SongsByAlbumAPIView.as_view()
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
