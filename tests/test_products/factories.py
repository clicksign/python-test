import factory
from factory.django import DjangoModelFactory
from faker import Faker

from products.models import Category, CategoryDiscount, Product

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = fake.text()


class CategoryDiscountFactory(DjangoModelFactory):
    class Meta:
        model = CategoryDiscount

    category = factory.SubFactory(CategoryFactory)
    discount_percentage = factory.Faker("random_int", min=0, max=100)
    product_quantity = factory.Faker("random_int", min=1, max=100)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = fake.text()
    price = factory.Faker("pydecimal", min_value=0, max_value=9999, right_digits=2)
    image = factory.Faker("image_url")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
