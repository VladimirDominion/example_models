import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from .models import Product, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('name')
    category = factory.SubFactory(CategoryFactory)
    price = factory.fuzzy.FuzzyDecimal(2.5, 42.7)
