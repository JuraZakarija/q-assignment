
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Product, ProductRating, CustomUser


class TestProduct(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='test_product',
            price='19.99'
        )
        self.admin_user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )
        self.test_user = CustomUser.objects.create(
                username='test_user',
                email='test@example.com',
                password='test'
            )

        self.list_url = reverse('products-list')
        self.detail_url = reverse(
            'products-detail',
            kwargs={'pk': self.product.id}
        )

    def test_products_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['price'], self.product.price)
        self.assertEqual(response.data['rating'], '0.00')

    def test_product_create_unauthorized(self):
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_create_authorized(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.list_url, {
            'name': 'test',
            'price': '19.19',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['price'], '19.19')

    def test_rate_product_unauthorized(self):
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '4',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rate_product_authorized(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '4',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 4)

    def test_rate_product_second_authorized(self):
        self.client = APIClient()
        # first user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '4',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # second user
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '5',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 4.5)

    def test_create_and_delete_rating(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '4',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 4)

        # check if rating is created correctly
        rating = ProductRating.objects.first()
        self.assertEqual(rating.user_id, self.admin_user.id)
        self.assertEqual(rating.product_id, self.product.id)
        self.assertEqual(rating.star_rating, 4)

        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.rating, 4)

        # delete rating and check if average rating is updated
        rating.delete()
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.rating, 0)

    def test_user_rating_same_product_twice(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # first user rating, success
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '4',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 4)

        # second user rating, error
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '2',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 4)

    def test_rating_create_and_update(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # first user rating
        response = self.client.post(f'{self.detail_url}rate-product/', {
            'star_rating': '2',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(id=self.product.id).rating, 2)

        rating = ProductRating.objects.first()
        rating.star_rating = 5
        rating.save()

        self.assertEqual(Product.objects.get(id=self.product.id).rating, 5)


class TestProductRatings(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='test_product',
            price='19.99'
        )
        self.admin_user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )

        self.list_url = reverse('product-ratings-list')

    def test_product_ratings_create(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'{self.list_url}', {
            'star_rating': '4',
            'product': self.product.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = ProductRating.objects.first()
        self.assertEqual(rating.user_id, self.admin_user.id)
        self.assertEqual(rating.product_id, self.product.id)
        self.assertEqual(rating.star_rating, 4)
