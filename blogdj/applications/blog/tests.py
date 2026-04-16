"""API tests for blog endpoints."""

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author
from .models import Blog
from .models import Category
from .models import Kword
from .models import Suscriptions


@override_settings(DEBUG=True)
class SeedBlogDataAPITests(APITestCase):
    def setUp(self):
        self.seed_url = reverse("blog_app:seed-basic")

    def test_seed_recreates_sample_data_with_default_count(self):
        response = self.client.post(self.seed_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created"]["categories"], 4)
        self.assertEqual(response.data["created"]["keywords"], 8)
        self.assertEqual(response.data["created"]["authors"], 5)
        self.assertEqual(response.data["created"]["blogs"], 20)
        self.assertEqual(response.data["created"]["suscriptions"], 20)

        self.assertEqual(Category.objects.count(), 4)
        self.assertEqual(Kword.objects.count(), 8)
        self.assertEqual(Author.objects.count(), 5)
        self.assertEqual(Blog.objects.count(), 20)
        self.assertEqual(Suscriptions.objects.count(), 20)

    def test_seed_replaces_existing_data_and_accepts_custom_count(self):
        self.client.post(self.seed_url, {"count": 4}, format="json")
        response = self.client.post(self.seed_url, {"count": 6}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created"]["blogs"], 6)
        self.assertEqual(response.data["created"]["suscriptions"], 6)
        self.assertEqual(Blog.objects.count(), 6)
        self.assertEqual(Suscriptions.objects.count(), 6)
        self.assertEqual(Category.objects.count(), 4)
        self.assertEqual(Kword.objects.count(), 8)
        self.assertEqual(Author.objects.count(), 5)

    @override_settings(DEBUG=False)
    def test_seed_endpoint_is_available_only_in_debug(self):
        response = self.client.post(self.seed_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
