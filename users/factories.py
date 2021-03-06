import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    email = factory.Faker('email')