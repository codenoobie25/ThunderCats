class SalesDatabase:
    def __init__(self, db):
        self.db = db

    def generate_receipt_number(self):
        import random
        while True:
            # Generate 4 random digits
            random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            receipt_num = f"THZ-{random_digits}"

            # Check if it already exists
            if not self.receipt_exists(receipt_num):
                return receipt_num

    def receipt_exists(self, receipt_number):
        """Check if receipt number already exists"""
        if not self.db: return False
        try:
            cursor = self.db.cursor()
            query = "SELECT COUNT(*) FROM sales WHERE receipt_number = %s"
            cursor.execute(query, (receipt_number,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"✗ Error checking receipt: {e}")
            return False

    def create_sale(self, subtotal, tax_amount, total_amount, payment_method, cash_tendered, change_amount):

        if not self.db: return None
        try:
            # Generate receipt number
            receipt_number = self.generate_receipt_number()

            cursor = self.db.cursor()
            query = """
                    INSERT INTO sales
                    (receipt_number, subtotal, tax_amount, total_amount, payment_method, cash_tendered, \
                     change_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) \
                    """
            cursor.execute(query,
                           (receipt_number, subtotal, tax_amount, total_amount, payment_method, cash_tendered,
                            change_amount))
            self.db.commit()

            sale_id = cursor.lastrowid
            print(f"✓ Sale created: ID={sale_id}, Receipt={receipt_number}")

            return {
                'sale_id': sale_id,
                'receipt_number': receipt_number
            }

        except Exception as e:
            print(f"✗ DB Error (Create Sale): {e}")
            self.db.rollback()
            return None

    def add_sale_details(self, sale_id, cart_items):
        if not self.db: return False
        try:
            cursor = self.db.cursor()
            query = """
                    INSERT INTO sale_details
                        (sale_id, product_id, quantity, subtotal, unit_price)
                    VALUES (%s, %s, %s, %s, %s) \
                    """

            for item in cart_items:
                cursor.execute(query, (
                    sale_id,
                    item['product_id'],
                    item['quantity'],
                    item['unit_price'],
                    item['subtotal']  # quantity * unit_price
                ))

            self.db.commit()
            print(f"✓ Added {len(cart_items)} items to sales_details")
            return True

        except Exception as e:
            print(f"✗ DB Error (Add Sale Details): {e}")
            import traceback
            traceback.print_exc()
            if self.db:
                self.db.rollback()
            return False

    def decrement_stock(self, cart_items):
        """Subtract sold items from product inventory"""
        if not self.db: return False
        try:
            cursor = self.db.cursor()
            query = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s"

            for item in cart_items:
                cursor.execute(query, (item['quantity'], item['product_id']))

            # Note: If you removed individual commits earlier, don't commit here.
            # If you kept them, add self.db.commit() here.
            return True
        except Exception as e:
            print(f"✗ DB Error (Stock Update): {e}")
            return False

    def complete_transaction(self, cart_items, payment_method, cash_tendered):

        if not cart_items:
            return None

        subtotal = sum(item['subtotal'] for item in cart_items)
        tax_rate = 0.08
        tax_amount = round(subtotal * tax_rate, 2)
        total_amount = round(subtotal + tax_amount, 2)
        change_amount = round(cash_tendered - total_amount, 2)

        sale_result = self.create_sale(
            subtotal, tax_amount, total_amount,
            payment_method, cash_tendered, change_amount
        )
        if not sale_result: return None

        if not self.add_sale_details(sale_result['sale_id'], cart_items):
            return None

        if not self.decrement_stock(cart_items):
            print("Warning: Failed to update stock levels")
            return None
        self.db.commit()

        return {
            'sale_id': sale_result['sale_id'],
            'receipt_number': sale_result['receipt_number'],
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'cash_tendered': cash_tendered,
            'change_amount': change_amount,
            'items': cart_items
        }