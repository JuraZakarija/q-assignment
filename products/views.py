from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductRating
from .serializers import (
    ProductListSerializer, ProductRatingListSerializer,
    ProductRatingCreateSerializer, ProductRatingDetailSerializer,
    ProductDetailSerializer, RateProductSerializer
)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'name', 'price', 'rating', 'updated_at']
    search_fields = ['id', 'name', 'price', 'rating', 'updated_at']

    @action(detail=True, methods=['post'], url_path='rate-product')
    def rate_product(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'rate_product':
            return RateProductSerializer
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class


class ProductRatingViewSet(ModelViewSet):
    serializer_class = ProductRatingDetailSerializer
    queryset = ProductRating.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductRatingListSerializer
        if self.action == 'create':
            return ProductRatingCreateSerializer
        return self.serializer_class
