from django.urls import path
from apps.api.views import ListArtistAPIView, DetailArtistAPIView


urlpatterns = [
    path(
        'artists/', ListArtistAPIView.as_view(), name='artists-list'
    ),
    path(
        'artists/<str:pk>/', DetailArtistAPIView.as_view(), name='artists-detail'
    ),
]
