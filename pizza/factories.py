import factory
from factory.django import DjangoModelFactory

from pizza.models import Pizza, Topping


class ToppingFactory(DjangoModelFactory):
    class Meta:
        model = Topping

    name = factory.Faker('name')


class PizzaFactory(DjangoModelFactory):
    class Meta:
        model = Pizza

    name = factory.Faker('name')