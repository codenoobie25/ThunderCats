import random
import string


class ProductsDatabase:
    def __init__(self, db):
        self.db = db

    def generate_sku(self):
        random_sku = ''.join(random.choices(string.digits, k=5))
        return f"SXU-{random_sku}"

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
            self.db.db.commit()
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

    def add_product(self,product_id,name, sku, categoryID, price, stock, warranty,status):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                INSERT INTO products (product_id, name, sku, price, status, stock_quantity, categoryID, warranty)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (product_id, name, sku, price, status, stock, categoryID, warranty))
            self.db.db.commit()
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
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return False

    def get_product_by_id(self,product_id):
        cursor = self.db.db.cursor()
        query = "select * from products where product_id = %s"
        cursor.execute(query, (product_id,))
        return cursor.fetchone()

    def generate_product_id(self):
        """Generate a unique 3-digit product ID (100-999)"""
        cursor = self.db.db.cursor()
        try:
            # Get the highest existing product ID
            cursor.execute("SELECT MAX(CAST(product_id AS UNSIGNED)) FROM products WHERE product_id REGEXP '^[0-9]+$'")
            result = cursor.fetchone()

            if result and result[0]:
                last_id = int(result[0])
                new_id = last_id + 1

                # If we've exceeded 999, start looking for gaps
                if new_id > 999:
                    cursor.execute("""
                                   SELECT product_id
                                   FROM products
                                   WHERE product_id REGEXP '^[0-9]+$' 
                        AND CAST(product_id AS UNSIGNED) BETWEEN 100 AND 999
                                   ORDER BY CAST (product_id AS UNSIGNED)
                                   """)
                    used_ids = {int(row[0]) for row in cursor.fetchall()}

                    # Find first available ID in 100-999 range
                    for i in range(100, 1000):
                        if i not in used_ids:
                            return str(i).zfill(3)

                    # If all IDs are used, raise error
                    raise Exception("All 3-digit product IDs are in use!")
            else:
                # Start with 100 if no products exist
                new_id = 100

            # Ensure it's 3 digits
            if new_id < 100:
                new_id = 100
            elif new_id > 999:
                raise Exception("Product ID exceeds 3-digit limit!")

            return str(new_id).zfill(3)

        except Exception as e:
            print(f"❌ Error generating product ID: {e}")
            return "100"  # Fallback to default
        finally:
            cursor.close()

    def fetch_inventory_list_data(self):
        if not self.db: return []
        try:
            cursor = self.db.cursor()
            query = """
                    SELECT p.name, \
                           p.sku,
                           c.categoryName, \
                           p.price, \
                           p.stock_quantity, \
                           p.warranty,
                           p.status
                    FROM products p
                             LEFT JOIN category c ON p.categoryID = c.categoryID
                    ORDER BY p.name ASC \
                    """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching inventory list data: {e}")
            return []

