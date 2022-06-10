from django.core.management.base import BaseCommand, CommandError
from products.models import Product, CustomUser
from products.factories import ProductFactory, UserFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Import started')
        
        print('Deleting old data')
        Product.objects.all().delete()

        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
            )
        print('Admin user created')
        
        UserFactory.create_batch(size=10)
        print('Fake users created')
        ProductFactory.create_batch(size=10)
        print('Fake products created')
