from django.contrib import admin

from .models import Category, Kword, Author, Blog,Suscriptions


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(Kword)
class KwordAdmin(admin.ModelAdmin):
    list_display = (
        'word',
        'num_searches',
        'id',
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'id',
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'resume',
        'date',
        'id',
    )
admin.site.register(Suscriptions)