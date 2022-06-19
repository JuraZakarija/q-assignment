from faker import Faker
from factory import LazyFunction, PostGenerationMethodCall
from factory.fuzzy import FuzzyDecimal
from factory.django import DjangoModelFactory

from .models import Product, CustomUser

fake = Faker(locale='hr_HR')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = LazyFunction(fake.bs)
    price = FuzzyDecimal(0, 100, 2)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = LazyFunction(fake.user_name)
    email = LazyFunction(fake.email)
    password = PostGenerationMethodCall('set_password', 'testing321')
