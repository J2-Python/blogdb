"""API views for subscriptions and sample data management."""

from typing import Any
from typing import cast

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Blog, Category, Suscriptions
from .serializers import AuthorSerializer
from .serializers import BlogCreateSerializer
from .serializers import BlogDetailSerializer
from .serializers import CategoryHiperLinkSerializer
from .serializers import CategorySerializer
from .serializers import SeedBlogDataSerializer
from .serializers import SuscriptionSerializer
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
        print("***desde la vista****")
        # print(serializer.data) da error
        print(serializer.validated_data["email"])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class BlogCreateView(CreateAPIView):
    """Create a blog from primitive values and return nested detail data."""

    # serializer de escritura
    serializer_class = BlogCreateSerializer
    # author es el campo FK y kwords y categorys son los campos m2m
    queryset = Blog.objects.select_related("author").prefetch_related(
        "kwords", "categorys"
    )

    # serializer para respuesta.
    response_serializer_class = BlogDetailSerializer

    # el metodo post ejecuta el metodo create()
    def create(self, request, *args, **kwargs):
        print(list(self.get_queryset()))
        qs=self.get_queryset()
        print("Count:",qs.count())
        print(qs.first())
        print(qs.values("id", "title"))
        print(list(qs.values("id", "title")))
        print("SQL:", qs.query)
        #!Paso 1: construir el serializer con los datos del request. Usa serializer_class que contiene el serializer BlogCreateSerializer.
        serializer = self.get_serializer(data=request.data)
        #!Paso 2: validar. is_valid() toma request.data y lo transforma en validated_data si todo sale bien. si es error lanza excepcion.
        serializer.is_valid(raise_exception=True)
        #! Paso 3: guardar. Aqui internamente se llama a serializer.save() que llama al metodo create() definido en el serializer.
        self.perform_create(serializer)
        #!en este punto el objeto blog ya esta creado, vuelvemos a consultar el blog con select_related y prefetch_related para tenerlo listo para serializar en detalle pero ya filtramos la consulta con get(pk=serializer.instance.pk). serializer.instance ya tienen el objeto que se grabo en bd.
        instance = (
            Blog.objects.select_related("author")
            .prefetch_related("kwords", "categorys")
            .get(pk=serializer.instance.pk)
        )
        #! aqui ya creamos un objeto de tipo BlogDetailSerializer que fue referenciado en la propiedad de la clase response_serializer_class
        response_serializer = self.response_serializer_class(
            instance,
            #! so le pasa información extra al serializer. Normalmente DRF incluye algo como: request, format, view. Es útil cuando el serializer necesita contexto externo. Por ejemplo: construir URLs absolutas, saber qué usuario hizo la petición, comportarse distinto según la vista
            context=self.get_serializer_context(),
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            #!  DRF convierte la instancia Blog en un diccionario serializado. Luego drf lo convierte al json final
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
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


class CrearSuscripcion(APIView):
    def post(self, request):
        serializer = SuscriptionSerializer(data=request.data)
        if serializer.is_valid():
            print("Guardar data")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Error serializador")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = BlogDetailSerializer
    queryset = Blog.objects.all()


class ListaAutores(ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class ListaCategorias(ListAPIView):
    # serializer_class=CategorySerializer
    serializer_class = CategoryHiperLinkSerializer
    queryset = Category.objects.all()


class CategoryDetail(RetrieveAPIView):
    lookup_field = "pz"
    serializer_class = CategorySerializer
    queryset = Category.objects.all
