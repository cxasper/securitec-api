from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from apps.api.models import Song, Artist


# Create your viewset tests here.
class SongsByArtistAPITestCase(APITestCase):
    def setUp(self):
        self.artist = mommy.make(Artist, _fill_optional=True)
        self.other_artist = mommy.make(Artist, _fill_optional=True)
        self.url = '/api/artists/{}/songs/'
        mommy.make(
            Song, album__artist=self.artist,
            _fill_optional=True, _quantity=20
        )

    def test_list(self):
        response = self.client.get(self.url.format(self.artist.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)

        # list with pagination
        response = self.client.get(
            self.url.format(self.artist.id), {'page': 2, 'page_size': 10},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        # list with other album
        response = self.client.get(self.url.format(self.other_artist.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
