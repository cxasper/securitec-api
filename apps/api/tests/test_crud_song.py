from random import randint
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from faker import Faker
from apps.api.models import Album, Song


fake = Faker()


# Create your viewset tests here.
class SongAPITestCase(APITestCase):
    def setUp(self):
        self.album = mommy.make(Album, _fill_optional=True)
        self.songs = mommy.make(
            Song, album=self.album,
            _fill_optional=True, _quantity=20
        )
        self.song_random = self.songs[randint(0, 19)]
        self.detail_url = reverse(
            'songs-detail',
            kwargs={'pk': self.song_random.pk}
        )
        user = User.objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='pass1234',
        )
        self.client.force_authenticate(user=user)
        self.list_url = reverse('songs-list')

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
            self.list_url, {'search': self.song_random.name},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'album': self.album.pk,
            'name': fake.name(),
            'duration': fake.time()
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('album' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('duration' in response.data)

    def test_partial_update(self):
        data = {
            'duration': fake.time()
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update(self):
        data = {
            'album': self.album.pk,
            'name': fake.name(),
            'duration': fake.time()
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
