import random
import string


class ProductsDatabase:
    def __init__(self, db):
        self.db = db

    def generate_sku(self):
        random_sku = ''.join(random.choices(string.digits, k=5))
        return f"SXU{random_sku}"

    def get_product_by_id(self, product_id):
        if not self.db: return None
        cursor = self.db.db.cursor()
        query = "SELECT * FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        return cursor.fetchone()

    def update_product(self, product_id, name, category_id, price, stock, warranty, status):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                UPDATE products 
                SET name=%s, categoryID=%s, price=%s, stock_quantity=%s, warranty=%s, Status=%s
                WHERE product_id=%s
            """
            cursor.execute(query, (name, category_id, price, stock, warranty, status, product_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return False

    def get_all_categories(self):
        if not self.db: return []
        cursor = self.db.db.cursor()
        query = "SELECT categoryID, categoryName FROM category"
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_products(self):
        if not self.db: return []
        cursor = self.db.db.cursor()
        query = """
            SELECT p.product_id, p.name, p.sku, c.categoryName, p.price, p.stock_quantity, p.Status, p.warranty
            FROM products p
            LEFT JOIN category c ON p.categoryID = c.categoryID
                """
        cursor.execute(query)
        return cursor.fetchall()
    def add_product(self, name, sku, category_id, price, stock, warranty,status="Active"):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                INSERT INTO products (name, sku, categoryID, price, stock_quantity, warranty)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (name, sku, category_id, price, stock, warranty, status))
            self.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return False
    def delete_product(self, product_id):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = "DELETE FROM products WHERE product_id = %s"  # Fixed 'product_id'
            cursor.execute(query, (product_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return False
    def get_product_by_id(self,product_id):
        cursor = self.db.db.cursor()
        query = "select * from products where product_id = %s"
        cursor.execute(query, (product_id,))
        return cursor.fetchone()

