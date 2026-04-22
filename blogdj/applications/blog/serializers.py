"""Serializers for blog API endpoints."""

from django.db import transaction

from rest_framework import serializers

from .models import Author, Blog, Category, Kword
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
        #! validated_data = { 'blog':'sdfsdfs','email':'juan@collantes.ec'} y es proporcionado por la clase Serializer
        # return Suscriptions.objects.create(**validated_data)
        print("****desde el serializer****")
        print(validated_data["blog"])
        #! por como esta definido el field blog como PrimaryKeyRelatedField al leer validated_data['blog'] ya devuelve una instancia de Blog
        blog = validated_data["blog"]
        # blog=Blog.objects.get(id=validated_data['blog'])
        print(validated_data["email"])
        email = validated_data["email"]
        return Suscriptions.objects.create(blog=blog, email=email)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class SeedBlogDataSerializer(serializers.Serializer):
    """Validate the amount of sample blog data to recreate."""

    #! Este serializador valida que el valor recibido en count el minimo sea uno, el maximo 100 y su valor por defecto en caso de que no se envie sea de 20.
    count = serializers.IntegerField(min_value=1, max_value=100, default=20)


#! Otra manera de validar es con funciones externas a las clases
def validar_blog(value):
    if not (Blog.objects.filter(id=value).exists()):
        raise serializers.ValidationError("error en id blog")
    return value


class SuscriptionSerializer(serializers.Serializer):
    blog = serializers.CharField(validators=[validar_blog])
    email = serializers.EmailField()
    # def validate(self,data):
    #     blog_id=data["blog"]
    #     if not (Blog.objects.filter(id=blog_id).exists()):
    #         raise serializers.ValidationError(f"el blog con id {blog_id} no existe")


class AuthorSerializer(serializers.ModelSerializer):
    #! num_blogs y full_name sera un campo calculado con SerializerMethodField(). El nombre del metodo tiene que ser el profijo get_ y el nombre del campo.
    num_blogs = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        # fields=('__all__')
        fields = ("id", "full_name", "email", "num_blogs")

    def get_num_blogs(self, obj):
        print(obj.id)
        blogs = Blog.objects.filter(author__id=obj.id).count()
        return blogs

    def get_full_name(self, obj):
        return obj.full_name.upper()


class KwordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kword
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryHiperLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("url",)
        extra_kwargs = {
            "url": {"view_name": "blog_app:category-detail", "lookup_field": "pk"}
        }


class BlogCreateSerializer(serializers.ModelSerializer):
    """Validate and create blogs from primitive input values."""

    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    kwords = serializers.PrimaryKeyRelatedField(
        queryset=Kword.objects.all(), many=True, allow_empty=False
    )
    categorys = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, allow_empty=False
    )

    class Meta:
        model = Blog
        fields = (
            "id",
            "author",
            "kwords",
            "categorys",
            "title",
            "resume",
            "image",
            "content",
            "date",
        )
        read_only_fields = ("id",)
    #! Despues de que el serializador haya ejecutado sus validaciones ejecuta los metodos personalizados. La convencion es validate_<nombre del campo>
    def validate_kwords(self, value):
        #!value tiene la lista de instancias de kwords ya validada y la recibe el argumento items de la funcion _validate_unique_related_items, field_name="kwords" la recibe el argumento field_name
        self._validate_unique_related_items(value, field_name="kwords")
        return value

    def validate_categorys(self, value):
        #!value tiene la lista de instancias de categorys ya validada y la recibe el argumento items de la funcion _validate_unique_related_items, field_name="categorys" la recibe el argumento field_name
        self._validate_unique_related_items(value, field_name="categorys")
        return value
    #! este es un helper. empieza con _ que por convencion signfica que el metodo solo se va a ejecutar dentro de la clase o para uso interno.
    def _validate_unique_related_items(self, items, *, field_name):
        
        item_ids = [item.pk for item in items]
        if len(item_ids) != len(set(item_ids)):
            raise serializers.ValidationError(
                f"No se permiten IDs repetidos en '{field_name}'."
            )

    def create(self, validated_data):
        #!validated_data es un diccionario.
        print(type(validated_data))
        #!Se obtiene el valor valor que tiene la llave kwords y categorys y al mismo tiempo quita esos elementos del diccionario"
        kwords = validated_data.pop("kwords")
        categorys = validated_data.pop("categorys")
        with transaction.atomic():
            #! primero se crea el objeto blog para poder asignar los campos manytomany
            blog = Blog.objects.create(**validated_data)
            blog.kwords.set(kwords)
            blog.categorys.set(categorys)
        return blog


class BlogDetailSerializer(serializers.ModelSerializer):
    # con esto le decimos a este serializador que cuando muestre el campo relacionado author y kwords muestre la informacion que esta configurada en el serializer AuthorSerializer, KwordSerializer y CategorySerializer. esto se usa para campos FK y para campos ManyToMany
    author = AuthorSerializer()
    kwords = KwordSerializer(many=True)
    categorys = CategorySerializer(many=True)

    class Meta:
        model = Blog
        fields = (
            "id",
            "author",
            "kwords",
            "categorys",
            "title",
            "resume",
            "image",
            "content",
            "date",
        )
