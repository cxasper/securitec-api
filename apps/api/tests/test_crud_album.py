from random import randint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from model_mommy.random_gen import gen_image_field
from faker import Faker
from apps.api.models import Artist, Album


fake = Faker()


# Create your viewset tests here.
class AlbumAPITestCase(APITestCase):
    fixtures = ['countries.json']

    def setUp(self):
        self.artist = mommy.make(Artist, _fill_optional=True)
        self.albums = mommy.make(
            Album, artist=self.artist,
            _fill_optional=True, _quantity=20
        )
        self.album_random = self.albums[randint(0, 19)]
        self.detail_url = reverse(
            'albums-detail',
            kwargs={'pk': self.album_random.pk}
        )
        self.list_url = reverse('albums-list')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)

        # list with pagination
        response = self.client.get(
            self.list_url, {'page': 2, 'page_size': 10},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        # list with search name
        response = self.client.get(
            self.list_url, {'search': self.album_random.name},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'artist': self.artist.pk,
            'name': fake.name(),
            'cover_page': gen_image_field(),
            'description': fake.text(),
            'release_year': fake.date()
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('artist' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('cover_page' in response.data)
        self.assertTrue('description' in response.data)
        self.assertTrue('release_year' in response.data)
        self.assertTrue('duration' in response.data)

    def test_partial_update(self):
        data = {
            'cover_page': gen_image_field(),
            'description': fake.text(),
            'release_year': fake.date()
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update(self):
        data = {
            'artist': self.artist.pk,
            'name': fake.name(),
            'cover_page': gen_image_field(),
            'description': fake.text(),
            'release_year': fake.date()
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
