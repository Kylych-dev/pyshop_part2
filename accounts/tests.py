from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser
from rest_framework import status

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_user')
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jwt', response.json())

    def test_logout_user(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'success')

    def test_login_user_invalid_password(self):
        invalid_password_data = {
            "email": self.user_data['email'],
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, invalid_password_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_user_invalid_email(self):
        invalid_email_data = {
            "email": "nonexistent@example.com",
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, invalid_email_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
