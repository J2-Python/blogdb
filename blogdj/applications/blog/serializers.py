"""Serializers for blog API endpoints."""

from rest_framework import serializers

from .models import Blog
from .models import Suscriptions


class SuscriberModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscriptions
        fields = "__all__"


class SuscriberSerializer(serializers.Serializer):
    """Serializer used by the lightweight subscription endpoint."""

    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    email = serializers.EmailField()

    def create(self, validated_data):
        return Suscriptions.objects.create(**validated_data)


class SeedBlogDataSerializer(serializers.Serializer):
    """Validate the amount of sample blog data to recreate."""
    #! Este serializador valida que el valor recibido en count el minimo sea uno, el maximo 100 y su valor por defecto en caso de que no se envie sea de 20.
    count = serializers.IntegerField(min_value=1, max_value=100, default=20)
