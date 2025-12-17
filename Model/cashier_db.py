
class CashierDatabase:
    def __init__(self, db):
        self.db = db

    def get_all_categories(self):
        """Get all product categories"""
        if not self.db: return []
        try:
            cursor = self.db.cursor()
            query = "SELECT categoryID, categoryName FROM category ORDER BY categoryName"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ DB Error (Get Categories): {e}")
            return []

    def get_available_products(self):
        """Get all products with stock > 0"""
        if not self.db: return []
        try:
            cursor = self.db.cursor()
            query = """
                    SELECT p.product_id, p.name, p.price, p.stock_quantity, p.categoryID
                    FROM products p
                    WHERE p.stock_quantity > 0
                    ORDER BY p.name \
                    """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ DB Error (Get Products): {e}")
            return []
