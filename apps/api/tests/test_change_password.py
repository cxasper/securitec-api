from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test@gmail.com', password='pass1234')
        self.change_password_url = reverse('rest_password_change')
        self.client.force_authenticate(user=self.user)

    def test_change_password(self):
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'old_password': 'pass1234'
        }
        response = self.client.post(
            self.change_password_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'detail': 'New password has been saved.'}
        )

    def test_change_password_with_invalid_old_pass(self):
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'old_password': 'invalid_old_pass'
        }
        response = self.client.post(
            self.change_password_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_when_new_pass_dont_match(self):
        data = {
            'new_password1': 'new_password',
            'new_password2': 'other_password',
            'old_password': 'pass1234'
        }
        response = self.client.post(
            self.change_password_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
