from rest_framework.filters import SearchFilter
from apps.api.paginations import CustomPagination
from apps.api.generics import ListAPIView, CreateAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from apps.api.models import Artist, Album, Song, Country
from apps.api.serializers import ArtistSerializer, AlbumSerializer, \
    SongSerializer, CountrySerializer


# Create your views here.
class ListCountryAPIView(ListAPIView):
    model = Country
    serializer_class = CountrySerializer
    pagination_class = CustomPagination


class ListArtistAPIView(ListAPIView, CreateAPIView):
    model = Artist
    serializer_class = ArtistSerializer
    pagination_class = CustomPagination
    search_class = SearchFilter
    search_fields = ['name']


class DetailArtistAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    model = Artist
    serializer_class = ArtistSerializer


class ListAlbumAPIView(ListAPIView, CreateAPIView):
    model = Album
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination
    search_class = SearchFilter
    search_fields = ['name']


class DetailAlbumAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    model = Album
    serializer_class = AlbumSerializer


class ListSongAPIView(ListAPIView, CreateAPIView):
    model = Song
    serializer_class = SongSerializer
    pagination_class = CustomPagination
    search_class = SearchFilter
    search_fields = ['name']


class DetailSongAPIView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    model = Song
    serializer_class = SongSerializer


class SongsByAlbumAPIView(ListAPIView):
    parent_model = Album
    model = Song
    serializer_class = SongSerializer
    pagination_class = CustomPagination

class SongsByArtistAPIView(ListAPIView):
    parent_model = Artist
    filter_parent = 'album__artist'
    model = Song
    serializer_class = SongSerializer
    pagination_class = CustomPagination


class AlbumsByArtistAPIView(ListAPIView):
    parent_model = Artist
    model = Album
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination
