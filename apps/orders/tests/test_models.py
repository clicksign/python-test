from decimal import Decimal
from django.db.models import ProtectedError
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.orders.models import Order, OrderItem
from apps.products.models import Product, Category

User = get_user_model()


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.material_category = Category.objects.create(id=1, name="Material Escolar")
        self.construction_category = Category.objects.create(id=4, name="Construção")
        self.other_category = Category.objects.create(name="Outra Categoria")
        self.order = None

    def create_product(self, name, price, category):
        return Product.objects.create(name=name, price=price, category=category)

    def create_order_item(self, product, quantity):
        return OrderItem.objects.create(product=product, quantity=quantity, order=self.order)

    def create_order(self, user):
        self.order = Order.objects.create(user=user, total=Decimal("0.00"))

    def recalculate_and_assert(self, expected_total):
        self.order.recalculate_total()
        order_items_total = sum([item.total for item in self.order.order_items.all()])
        self.assertEqual(self.order.total, expected_total)
        self.assertEqual(self.order.total, order_items_total)

    def test_recalculate_total_without_discount(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.other_category)
        order_item = self.create_order_item(product, 2)
        self.recalculate_and_assert(order_item.total)

    def test_recalculate_total_with_material_category_discount(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.material_category)
        self.create_order_item(product, 2)
        self.recalculate_and_assert(Decimal("17.00"))

    def test_recalculate_total_with_construction_category_discount_3_items(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.construction_category)
        self.create_order_item(product, 3)
        self.recalculate_and_assert(Decimal('28.50'))

    def test_recalculate_total_with_construction_category_discount_5_items(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.construction_category)
        self.create_order_item(product, 5)
        self.recalculate_and_assert(Decimal('46.50'))

    def test_recalculate_total_with_construction_category_discount_multiple_items(self):
        self.create_order(self.user)
        product1 = self.create_product("Product 1", Decimal("10.00"), self.construction_category)
        product2 = self.create_product("Product 2", Decimal("15.00"), self.construction_category)
        order_item1 = self.create_order_item(product1, 2)
        order_item2 = self.create_order_item(product2, 3)
        self.recalculate_and_assert(order_item1.total + order_item2.total)

    def test_recalculate_total_without_discount_multiple_items(self):
        self.create_order(self.user)
        product1 = self.create_product("Product 1", Decimal("10.00"), self.other_category)
        product2 = self.create_product("Product 2", Decimal("15.00"), self.other_category)
        order_item1 = self.create_order_item(product1, 2)
        order_item2 = self.create_order_item(product2, 3)
        self.recalculate_and_assert(order_item1.total + order_item2.total)

    def test_product_protected_deletion(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.other_category)
        self.create_order_item(product, 2)
        self.recalculate_and_assert(product.price * 2)

        product_id = product.id
        with self.assertRaises(ProtectedError):
            product.delete()

        # Ensure the product is still present in the order item
        order_item = OrderItem.objects.get(product_id=product_id)
        self.assertEqual(order_item.product_id, product_id)

        self.recalculate_and_assert(product.price * 2)

    def test_category_protected_deletion(self):
        self.create_order(self.user)
        product = self.create_product("Product 1", Decimal("10.00"), self.other_category)
        order_item = self.create_order_item(product, 2)
        self.recalculate_and_assert(order_item.total)

        category_id = self.other_category.id
        with self.assertRaises(ProtectedError):
            self.other_category.delete()

        # Ensure the category is still present in the order item
        order_item = OrderItem.objects.get(product_id=product.id)
        self.assertEqual(order_item.product.category_id, category_id)

        self.recalculate_and_assert(order_item.total)
