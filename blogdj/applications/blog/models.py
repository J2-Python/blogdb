from django.db import models


# Create your models here.
class Category(models.Model):
    MAIN = "0"
    SECONDARY = "1"

    TYPE_CHOICES = [
        (MAIN, "principal"),
        (SECONDARY, "secundaria"),
    ]

    name = models.CharField(
        "nombre",
        max_length=40,
    )
    type_category = models.CharField("tipo", max_length=2, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Kword(models.Model):

    word = models.CharField(
        "palabra clave",
        max_length=40,
    )
    num_searches = models.PositiveIntegerField("numero de busquedas")

    class Meta:
        verbose_name = "Palabra Clave"
        verbose_name_plural = "Palabras Clave"

    def __str__(self):
        return self.word


class Author(models.Model):

    full_name = models.CharField(
        "Nombres",
        max_length=100,
    )
    email = models.EmailField("E-mail")
    avatar = models.ImageField("Avatar", upload_to="avatars", blank=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.full_name


class Blog(models.Model):

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Autor",
    )
    kwords = models.ManyToManyField(
        Kword,
        related_name="kwords",
        verbose_name="claves",
    )
    categorys = models.ManyToManyField(
        Category,
        related_name="categorys",
        verbose_name="categorias",
    )
    title = models.CharField(
        "Titulo",
        max_length=100,
    )
    resume = models.CharField("resumen", max_length=150)
    image = models.ImageField("portada", upload_to="blog_imgs", blank=True)
    content = models.TextField("contenido")
    date = models.DateTimeField(
        "Fecha-Hora",
    )

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return self.title


class Suscriptions(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    email = models.EmailField("Correo", max_length=254)

    class Meta:
        verbose_name = "Suscripcion"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        return self.email
