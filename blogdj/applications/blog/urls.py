from django.urls import path

from .views import AgregarSuscripcion, BlogCreateView, BlogDetail, CategoryDetail, CrearSuscripcion, ListaAutores, ListaCategorias
from .views import RegistrarSuscripcion
from .views import SeedBlogDataView


app_name = "blog_app"

urlpatterns = [
    path(
        "api/suscriptions/register/",
        RegistrarSuscripcion.as_view(),
        name="register-suscription",
    ),
    path(
        "api/suscriptions/add/",
        AgregarSuscripcion.as_view(),
        name="add-suscription",
    ),
    path(
        "api/seed/basic/",
        SeedBlogDataView.as_view(),
        name="seed-basic",
    ),
    path(
        "api/suscriptions/create/",
        CrearSuscripcion.as_view(),
        name="add-suscription",
    ),
    path(
        "api/blog/detail/<pk>",
        BlogDetail.as_view(),
        name="blog_detail",
    ),
    path(
        "api/blog/create/",
        BlogCreateView.as_view(),
        name="blog-create",
    ),
    path(
        "api/blog/list/",
        ListaAutores.as_view(),
        name="lista_autores",
    ),
    path(
        "api/category/list/",
        ListaCategorias.as_view(),
        name="lista_categorias",
    ),
    path(
        "api/category/detail/<pk>/",
        CategoryDetail.as_view(),
        name="category-detail",
    ),
]
