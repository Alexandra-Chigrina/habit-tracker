from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from django.urls import reverse


User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.password = "pass1234"
        self.user = User.objects.create(email="user@example.com", password=self.password)
        self.user.set_password(self.password)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:profile")

    def test_user_retrieve_own_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_create(self):
        self.client.logout()
        url = reverse("users:register")
        data = {"email": "new@example.com", "password": "pass1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.logout()
        url = reverse("users:login")
        data = {"email": self.user.email, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class CreateAdminCommandTest(TestCase):
    def test_create_admin_user(self):
        self.assertFalse(User.objects.filter(email="a.chigrina1989@gmail.com").exists())
        call_command("createadmin")
        user = User.objects.get(email="a.chigrina1989@gmail.com")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("Zxcv1234"))
