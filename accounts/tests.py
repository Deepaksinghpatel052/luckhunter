from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import LsUser


def make_user(email='jane@example.com', password='StrongPass123', **overrides):
    user = User.objects.create_user(username=email, email=email, password=password)
    defaults = {'name': 'Jane Doe', 'Contact_no': 9998887777, 'status': True}
    defaults.update(overrides)
    ls_user = LsUser.objects.create(user=user, **defaults)
    return user, ls_user


class RegisterAPITests(APITestCase):
    def test_register_success(self):
        response = self.client.post(reverse('api:accounts_api:register'), {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john@example.com',
            'phone_no': 1234567890,
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='john@example.com').exists())
        self.assertTrue(LsUser.objects.filter(Contact_no=1234567890).exists())

    def test_register_duplicate_email(self):
        make_user(email='dup@example.com')

        response = self.client.post(reverse('api:accounts_api:register'), {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'dup@example.com',
            'phone_no': 1234567890,
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_phone(self):
        make_user(Contact_no=1112223333)

        response = self.client.post(reverse('api:accounts_api:register'), {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'unique@example.com',
            'phone_no': 1112223333,
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('api:accounts_api:register'), {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'unique2@example.com',
            'phone_no': 1234509876,
            'password': 'StrongPass123',
            'confirm_password': 'Different123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPITests(APITestCase):
    def test_login_success_returns_tokens(self):
        make_user(email='login@example.com', password='StrongPass123')

        response = self.client.post(reverse('api:accounts_api:login'), {
            'email': 'login@example.com',
            'password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        make_user(email='login2@example.com', password='StrongPass123')

        response = self.client.post(reverse('api:accounts_api:login'), {
            'email': 'login2@example.com',
            'password': 'WrongPassword',
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_disabled_account(self):
        make_user(email='disabled@example.com', password='StrongPass123', status=False)

        response = self.client.post(reverse('api:accounts_api:login'), {
            'email': 'disabled@example.com',
            'password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeAPITests(APITestCase):
    def test_me_requires_authentication(self):
        response = self.client.get(reverse('api:accounts_api:me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_with_valid_token(self):
        make_user(email='me@example.com', password='StrongPass123', name='Me Example')

        login_response = self.client.post(reverse('api:accounts_api:login'), {
            'email': 'me@example.com',
            'password': 'StrongPass123',
        })
        access = login_response.data['access']

        response = self.client.get(
            reverse('api:accounts_api:me'),
            HTTP_AUTHORIZATION=f'Bearer {access}',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'me@example.com')
        self.assertEqual(response.data['name'], 'Me Example')


class TokenRefreshAPITests(APITestCase):
    def test_refresh_token_returns_new_access_token(self):
        make_user(email='refresh@example.com', password='StrongPass123')

        login_response = self.client.post(reverse('api:accounts_api:login'), {
            'email': 'refresh@example.com',
            'password': 'StrongPass123',
        })
        refresh = login_response.data['refresh']

        response = self.client.post(reverse('api:accounts_api:token-refresh'), {'refresh': refresh})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
