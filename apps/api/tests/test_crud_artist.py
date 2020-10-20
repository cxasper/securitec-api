from random import randint
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from faker import Faker
from apps.api.models import Artist


fake = Faker()


# Create your viewset tests here.
class ArtistAPITestCase(APITestCase):
    fixtures = ['countries.json']

    def setUp(self):
        self.country_id = randint(1, 200)
        self.artists = mommy.make(
            Artist, country_id=self.country_id,
            _fill_optional=True, _quantity=20
        )
        self.artist_random = self.artists[randint(0, 19)]
        self.detail_url = reverse(
            'artists-detail',
            kwargs={'pk': self.artist_random.pk}
        )
        user = User.objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='pass1234',
        )
        self.client.force_authenticate(user=user)
        self.list_url = reverse('artists-list')

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
            self.list_url, {'search': self.artist_random.name},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'country': randint(1, 200),
            'name': fake.name(),
            'about': fake.text()
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('country' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('about' in response.data)

    def test_partial_update(self):
        data = {
            'country': randint(1, 200),
            'name': fake.name(),
            'about': fake.text()
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update(self):
        data = {
            'country': randint(1, 200),
            'name': fake.name(),
            'about': fake.text()
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
