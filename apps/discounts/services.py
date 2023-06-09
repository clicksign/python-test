class DiscountService:
    @classmethod
    def calculate_discount(cls, product_category_id, quantity):
        from apps.discounts.models import Discount

        discount_instance = (
            Discount.objects
            .filter(category__id=product_category_id, mininum_quantity__lte=quantity)
            .order_by('-mininum_quantity')
            .first()
        )

        if discount_instance is None:
            return 0

        return discount_instance.discount
