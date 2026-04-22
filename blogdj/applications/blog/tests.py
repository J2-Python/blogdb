"""API tests for blog endpoints."""

from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
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


class BlogCreateAPITests(APITestCase):
    def setUp(self):
        self.create_url = reverse("blog_app:blog-create")
        self.author = Author.objects.create(
            full_name="Autor Demo",
            email="autor@example.com",
        )
        self.category_one = Category.objects.create(
            name="Python",
            type_category=Category.MAIN,
        )
        self.category_two = Category.objects.create(
            name="APIs",
            type_category=Category.SECONDARY,
        )
        self.keyword_one = Kword.objects.create(word="django", num_searches=10)
        self.keyword_two = Kword.objects.create(word="drf", num_searches=20)
        self.payload = {
            "author": self.author.pk,
            "kwords": [self.keyword_one.pk, self.keyword_two.pk],
            "categorys": [self.category_one.pk, self.category_two.pk],
            "title": "Creando blogs en DRF",
            "resume": "Resumen de prueba para el endpoint.",
            "content": "Contenido de prueba del blog.",
            "date": timezone.now().isoformat(),
        }

    def test_create_blog_with_valid_related_ids_returns_nested_detail(self):
        response = self.client.post(self.create_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)

        blog = Blog.objects.get()
        self.assertEqual(blog.author, self.author)
        self.assertCountEqual(
            blog.kwords.values_list("id", flat=True),
            [self.keyword_one.pk, self.keyword_two.pk],
        )
        self.assertCountEqual(
            blog.categorys.values_list("id", flat=True),
            [self.category_one.pk, self.category_two.pk],
        )

        self.assertEqual(response.data["id"], blog.pk)
        self.assertEqual(response.data["author"]["id"], self.author.pk)
        self.assertEqual(response.data["author"]["email"], self.author.email)
        self.assertEqual(len(response.data["kwords"]), 2)
        self.assertEqual(len(response.data["categorys"]), 2)
        self.assertEqual(response.data["title"], self.payload["title"])

    def test_create_blog_returns_error_when_author_does_not_exist(self):
        payload = {**self.payload, "author": 9999}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("author", response.data)

    def test_create_blog_returns_error_when_keyword_does_not_exist(self):
        payload = {**self.payload, "kwords": [self.keyword_one.pk, 9999]}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("kwords", response.data)

    def test_create_blog_returns_error_when_category_does_not_exist(self):
        payload = {**self.payload, "categorys": [self.category_one.pk, 9999]}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categorys", response.data)

    def test_create_blog_returns_error_when_related_fields_are_empty(self):
        payload = {**self.payload, "kwords": [], "categorys": []}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("kwords", response.data)
        self.assertIn("categorys", response.data)

    def test_create_blog_returns_error_when_related_ids_are_repeated(self):
        payload = {
            **self.payload,
            "kwords": [self.keyword_one.pk, self.keyword_one.pk],
            "categorys": [self.category_one.pk, self.category_one.pk],
        }

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["kwords"][0],
            "No se permiten IDs repetidos en 'kwords'.",
        )
        self.assertEqual(
            response.data["categorys"][0],
            "No se permiten IDs repetidos en 'categorys'.",
        )

    def test_create_blog_returns_error_when_required_field_is_missing(self):
        payload = self.payload.copy()
        payload.pop("title")

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_blog_returns_error_when_related_fields_are_not_lists(self):
        payload = {**self.payload, "kwords": self.keyword_one.pk, "categorys": "1"}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("kwords", response.data)
        self.assertIn("categorys", response.data)

    def test_create_blog_returns_error_when_date_is_invalid(self):
        payload = {**self.payload, "date": "fecha-invalida"}

        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
