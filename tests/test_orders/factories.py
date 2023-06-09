import factory
from factory.django import DjangoModelFactory

from orders.models import Order, OrderItem
from tests.test_products.factories import ProductFactory
from tests.test_users.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    order_number = factory.Sequence(lambda n: n)
    customer = factory.SubFactory(UserFactory)
    total_amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    unit_price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    discount_amount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    subtotal = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
