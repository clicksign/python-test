import factory
from django.contrib.auth.models import User

from users.models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    role = "buyer"
    phone_number = factory.Faker("phone_number", locale="pt_BR")
    address = factory.Faker("address")
