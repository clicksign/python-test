class DiscountService:
    # TODO: Refactor this to use a database table instead of a hard-coded dict
    DISCOUNTS = {
        '1': 15,  # Category 1 gets a 15% discount
        '4': {    # Category 4 has discounts based on quantity
            '3': 5,   # 3 or more items gets a 5% discount
            '5': 7    # 5 or more items gets a 7% discount
        }
    }

    @classmethod
    def calculate_discount(cls, product_category_id, quantity):
        category_id = str(product_category_id)
        if category_id in cls.DISCOUNTS:
            discount = cls.DISCOUNTS[category_id]
            if isinstance(discount, dict):
                # Find the highest quantity that is less than or equal to the actual quantity
                applicable_quantities = [q for q in discount.keys() if int(q) <= quantity]
                if applicable_quantities:
                    # Get the discount corresponding to the highest quantity
                    highest_quantity = max(applicable_quantities, key=int)
                    return discount[highest_quantity]
            else:
                # If the discount is not a dict, then it's a flat rate discount
                return discount
        return 0
