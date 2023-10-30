"""
    Tests for User APIs
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
GENERATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """ Create User Helper function """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Tests for public features of the API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is successful. """
        payload = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_email_exist(self):
        """ Test creating a user is existing email. """
        payload = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        """ Test creating a user is with password less than 5 characters. """
        payload = {
            'email': "test@example.com",
            'password': '124',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exist)

    def test_generate_user_token(self):
        """ Test creating a user token. """
        user_details = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**user_details)
        payload = {
            'email': "test@example.com",
            'password': 'testpass123'
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_generate_token_bad_credentials(self):
        """ Test creating a user token with bad credentials """
        user_details = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**user_details)
        payload = {
            'email': "test@example.com",
            'password': 'badpass'
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_generate_token_blank_password(self):
        """ Test creating a user token with blank password."""
        user_details = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**user_details)
        payload = {
            'email': "test@example.com",
            'password': ''
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_user_profile_unauthorized(self):
        """ Test fetching user profile without authentication"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Tests for private features of the API """

    def setUp(self):
        user_details = {
            'email': "test@example.com",
            'password': 'testpass123',
            'name': 'Test Name'
        }
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_retrieve_success(self):
        """ Test fetching user profile """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_profile_post_method(self):
        """ Test post method on me url """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_update_success(self):
        """ Test Profile update  """
        payload = {
            'password': 'testnewpass',
            'name': 'New name'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
