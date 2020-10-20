from rest_framework.filters import SearchFilter
from apps.api.paginations import CustomPagination
from apps.api.generics import ListAPIView, CreateAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from apps.api.models import Artist, Album
from apps.api.serializers import ArtistSerializer, AlbumSerializer



# Create your views here.
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
