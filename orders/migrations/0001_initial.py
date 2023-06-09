import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("order_number", models.PositiveIntegerField(editable=False, unique=True)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("discount_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="products.product"),
                ),
            ],
        ),
    ]
