from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter


from .views import ProductViewSet, ProductRatingViewSet

router = DefaultRouter()
router.register(
    'products',
    ProductViewSet,
    basename='products'
)

router.register(
    'product-ratings',
    ProductRatingViewSet,
    basename='product-ratings'
)

urlpatterns = [
    path('', include(router.urls))
]
