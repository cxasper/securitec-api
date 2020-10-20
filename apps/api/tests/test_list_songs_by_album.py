from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from apps.api.models import Album, Song


# Create your viewset tests here.
class SongsByAlbumAPITestCase(APITestCase):
    def setUp(self):
        self.album = mommy.make(Album, _fill_optional=True)
        self.other_album = mommy.make(Album, _fill_optional=True)
        self.url = '/api/albums/{}/songs/'
        mommy.make(
            Song, album=self.album,
            _fill_optional=True, _quantity=20
        )

    def test_list(self):
        response = self.client.get(self.url.format(self.album.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)

        # list with pagination
        response = self.client.get(
            self.url.format(self.album.id), {'page': 2, 'page_size': 10},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        # list with other album
        response = self.client.get(self.url.format(self.other_album.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
