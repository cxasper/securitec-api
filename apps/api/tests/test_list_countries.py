from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your viewset tests here.
class CountryAPITestCase(APITestCase):
    fixtures = ['countries.json']

    def setUp(self):
        self.list_url = reverse('countries-list')

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
