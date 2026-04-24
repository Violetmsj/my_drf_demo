from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthApiTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("accounts:auth-register")
        self.login_url = reverse("accounts:auth-login")
        self.logout_url = reverse("accounts:auth-logout")
        self.me_url = reverse("accounts:auth-me")
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="existing_user",
            password=self.password,
        )

    def test_register_success(self):
        response = self.client.post(
            self.register_url,
            {"username": "new_user", "password": "AnotherPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "new_user")
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_with_duplicate_username_should_fail(self):
        response = self.client.post(
            self.register_url,
            {"username": "existing_user", "password": "AnotherPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"username": "existing_user", "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "existing_user")

    def test_login_with_invalid_credentials_should_fail(self):
        response = self.client.post(
            self.login_url,
            {"username": "existing_user", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_get_current_user_success(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "existing_user")

    def test_logout_should_invalidate_current_token(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.logout_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=token.key).exists())

        me_response = self.client.get(self.me_url)
        self.assertEqual(me_response.status_code, status.HTTP_401_UNAUTHORIZED)

