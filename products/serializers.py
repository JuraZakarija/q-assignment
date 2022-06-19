from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault,
    StringRelatedField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
)

from .models import Product, ProductRating


class CurrentProductDefault:
    """
    sets product from url as default product when rating from rate-product
    endpoint
    """

    requires_context = True

    def __call__(self, serializer_field):
        product_pk = (
            serializer_field.context["request"].parser_context.get(
                "kwargs").get("pk")
        )
        product = Product.objects.get(pk=product_pk)
        return product

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class ProductListSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="products-detail")
    ratings = HyperlinkedRelatedField(
        many=True, read_only=True, view_name="product-ratings-detail"
    )

    class Meta:
        model = Product
        fields = ["url", "id", "name", "price",
                  "rating", "updated_at", "ratings"]
        read_only_fields = ["rating", "updated_at"]


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "rating", "updated_at"]
        read_only_fields = ["rating", "updated_at"]


class RateProductSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    product = HiddenField(default=CurrentProductDefault())

    class Meta:
        model = ProductRating
        fields = ["id", "user", "product", "star_rating"]


class ProductRatingListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="product-ratings-detail")
    product = HyperlinkedRelatedField(
        view_name="products-detail", read_only=True)
    user = StringRelatedField()

    class Meta:
        model = ProductRating
        fields = ["url", "id", "user", "product", "star_rating"]


class ProductRatingDetailSerializer(ModelSerializer):
    user = StringRelatedField()
    product = StringRelatedField()

    class Meta:
        model = ProductRating
        fields = ["id", "user", "product", "star_rating"]
        read_only_fields = ["user", "product"]


class ProductRatingCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ProductRating
        fields = ["id", "user", "product", "star_rating"]
