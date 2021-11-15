from django.core.management.base import BaseCommand
from catalog.factories import CategoryFactory, ProductFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        CategoryFactory.create_batch(10)