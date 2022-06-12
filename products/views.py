from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
)
from .models import Product, ProductRating
from .serializers import (
    ProductSerializer, ProductRatingListSerializer, ProductRatingSerializer
)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'name', 'price', 'rating', 'updated_at']

    @action(detail=False, methods=['post'], url_path='rate-product')
    def rate_product(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'rate_product':
            return ProductRatingSerializer
        return super().get_serializer_class()


class ProductRatingViewSet(ListModelMixin,
                           RetrieveModelMixin,
                           UpdateModelMixin,
                           DestroyModelMixin,
                           GenericViewSet):
    serializer_class = ProductRatingListSerializer
    queryset = ProductRating.objects.all()
