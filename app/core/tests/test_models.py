"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user email normalized"""

        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected_email)

    def test_creating_user_without_email_raises_error(self):
        """Test Creating a User without email address will raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_super_user(self):
        """Test Creation of Super User"""
        user = get_user_model().objects.create_superuser(
            'test@example',
            'test123'
        )

        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_superuser, True)
