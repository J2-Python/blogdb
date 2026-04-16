from django.urls import path

from .views import AgregarSuscripcion
from .views import RegistrarSuscripcion
from .views import SeedBlogDataView

app_name = "blog_app"

urlpatterns = [
    path(
        "api/suscriptions/register",
        RegistrarSuscripcion.as_view(),
        name="register-suscription",
    ),
    path(
        "api/suscriptions/add",
        AgregarSuscripcion.as_view(),
        name="add-suscription",
    ),
    path(
        "api/seed/basic",
        SeedBlogDataView.as_view(),
        name="seed-basic",
    ),
]
