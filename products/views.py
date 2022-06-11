from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'name', 'price', 'rating', 'updated_at']
