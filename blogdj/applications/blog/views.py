"""API views for subscriptions and sample data management."""

from typing import Any
from typing import cast

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Suscriptions
from .serializers import SeedBlogDataSerializer
from .serializers import SuscriberModelSerializer
from .serializers import SuscriberSerializer
from .services import reset_blog_sample_data


class RegistrarSuscripcion(CreateAPIView):
    serializer_class = SuscriberModelSerializer
    queryset = Suscriptions.objects.all()


class AgregarSuscripcion(CreateAPIView):
    
    serializer_class = SuscriberSerializer
    queryset = Suscriptions.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('***desde la vista****')
        #print(serializer.data) da error
        print(serializer.validated_data['email'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SeedBlogDataView(APIView):
    """Reset and recreate sample data for the educational blog project."""

    #! se crea asigna el serializer a la clase pero como se esta usando una APIView el serializer que realmente se usa para validar el input de datos es el serializer que esta en el metodo post.
    serializer_class = SeedBlogDataSerializer

    def post(self, request, *args, **kwargs):
        # The seed endpoint is intentionally limited to local development.
        #! solo se ejecuta el seed si settings.DEBUG=true
        if not settings.DEBUG:
            raise PermissionDenied(
                "El endpoint de seed solo esta disponible cuando DEBUG=True."
            )
        #! este es el serializer que si valida los datos recibidos en la request
        serializer = SeedBlogDataSerializer(data=request.data)
        #! Si los datos son validos continua con la ejecucion, caso contrario lanza la excepcion
        serializer.is_valid(raise_exception=True)
        #!solamente si los datos fueron validados por el serializer se almacenan en validated_data como un diccionario.
        validated_data = cast(dict[str, Any], serializer.validated_data)
        #! obtenemos el valor de la clave count del diccionario
        count = int(validated_data["count"])
        #! ejecutamos el servicio enviando como parametro el numero de suscripciones que se van a crear
        created_data = reset_blog_sample_data(
            count=count,
        )
        #!respuesta de la api Response transforma el diccionario a json
        return Response(
            {
                "message": "Datos de prueba recreados correctamente.",
                "created": created_data,
            },
            status=status.HTTP_201_CREATED,
        )
