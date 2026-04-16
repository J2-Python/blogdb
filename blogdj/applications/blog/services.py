"""Service helpers for blog sample data generation."""

from __future__ import annotations

from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import Author
from .models import Blog
from .models import Category
from .models import Kword
from .models import Suscriptions

#!crea una lista de tuplas
CATEGORY_FIXTURES = [
    ("Python", Category.MAIN),
    ("Django", Category.MAIN),
    ("APIs", Category.SECONDARY),
    ("Tutoriales", Category.SECONDARY),
]
#!crea una lista de tuplas
KEYWORD_FIXTURES = [
    ("python", 120),
    ("django", 95),
    ("drf", 80),
    ("serializers", 60),
    ("views", 55),
    ("models", 50),
    ("postgres", 40),
    ("testing", 35),
]
#! Lista de tuplas
AUTHOR_FIXTURES = [
    ("Ana Torres", "ana@example.com"),
    ("Luis Perez", "luis@example.com"),
    ("Maria Gomez", "maria@example.com"),
    ("Carlos Ruiz", "carlos@example.com"),
    ("Elena Diaz", "elena@example.com"),
]

#!metodo que devuelve un string que es el contenido del post o blog
def _build_blog_content(index: int, author: Author) -> str:
    """Create readable body text for a sample post."""

    return (
        f"Este articulo de ejemplo #{index} fue escrito por {author.full_name}. "
        "Su objetivo es poblar el proyecto educativo con datos sencillos para "
        "probar listados, relaciones y endpoints en Django REST Framework. "
        "El contenido se mantiene simple para que el seed sea facil de entender "
        "y de mantener."
    )

#! Con esto definimos una transaccion atomica
@transaction.atomic
def reset_blog_sample_data(count: int = 20) -> dict[str, int]:
    """Delete existing blog data and recreate a small deterministic dataset."""
    #!Borramos todos los objetos(retistros) de todos los modelos
    Suscriptions.objects.all().delete()
    Blog.objects.all().delete()
    Author.objects.all().delete()
    Kword.objects.all().delete()
    Category.objects.all().delete()

    #!Crea una lista de Intancias Categoy
    categories = [
        #!por cada iteracion crea una Category. create() devuelve una instancia de Category
        #! por cada elemento iterado lo asigna a las variables name, type_category
        Category.objects.create(name=name, type_category=type_category)
        for name, type_category in CATEGORY_FIXTURES
    ]
    keywords = [
        Kword.objects.create(word=word, num_searches=num_searches)
        for word, num_searches in KEYWORD_FIXTURES
    ]
    authors = [
        Author.objects.create(full_name=full_name, email=email)
        for full_name, email in AUTHOR_FIXTURES
    ]

    base_date = timezone.now()#2026-04-16 10:35:42.123456+00:00
    subscriptions_to_create = []

    for index in range(count):
        #!obtiene un autor
        author = authors[index % len(authors)]
        #!obtiene una categoria primaria y otra secundaria
        primary_category = categories[index % len(categories)]
        secondary_category = categories[(index + 1) % len(categories)]
        #!obtiene una keyword primaria y otra secundaria
        primary_keyword = keywords[index % len(keywords)]
        secondary_keyword = keywords[(index + 2) % len(keywords)]
        #! creo un blog por cada iteracion con sus fields necesarios
        blog = Blog.objects.create(
            author=author,
            title=f"Post de prueba {index + 1}",
            resume=(
                f"Resumen corto del post de prueba {index + 1} para validar "
                "datos de ejemplo."
            ),
            content=_build_blog_content(index + 1, author),
            date=base_date - timedelta(days=index),
        )
        #! Asigna relaciones many-to-many al blog, Dos categorías, Dos keywords.
        blog.categorys.set([primary_category, secondary_category])
        blog.kwords.set([primary_keyword, secondary_keyword])
        #! asignamos a la lista subscriptions_to_create istancias de Suscriptions estan en memoria y no estan persistente que se inicializan en cada iteracion.
        subscriptions_to_create.append(
            Suscriptions(
                blog=blog,
                email=f"lector{index + 1:02d}@example.com",
            )
        )
    #! se crean masivamente todas las instancias que estan en la lista.
    Suscriptions.objects.bulk_create(subscriptions_to_create)

    return {
        "categories": len(categories),
        "keywords": len(keywords),
        "authors": len(authors),
        "blogs": count,
        "suscriptions": len(subscriptions_to_create),
    }
