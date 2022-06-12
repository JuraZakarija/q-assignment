from rest_framework.serializers import (
    ModelSerializer, HiddenField, CurrentUserDefault, StringRelatedField,
    HyperlinkedModelSerializer, HyperlinkedIdentityField,
)

from .models import Product, ProductRating


class ProductSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='products-detail')

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'price', 'rating', 'updated_at']
        read_only_fields = ['rating', 'updated_at']


class ProductRatingSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ProductRating
        fields = ['id', 'user', 'product', 'star_rating']

    def create(self, validated_data):
        return super().create(validated_data)


class ProductRatingListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='product-ratings-detail')
    product = StringRelatedField()
    user = StringRelatedField()

    class Meta:
        model = ProductRating
        fields = ['url', 'id', 'user', 'product', 'star_rating']
