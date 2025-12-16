import pymysql

class AdminDatabase:
    def __init__(self, db):
        self.db = db
    def get_category_counts(self):

        cursor = self.db.cursor()
        try:
            # Assumes your table is named 'products' and has a 'Category' column
            query = "SELECT categoryID, COUNT(*) FROM products GROUP BY categoryID"
            cursor.execute(query)
            results = cursor.fetchall()

            category_map = {
                101: 'GPU',
                102: 'CPU',
                103: 'Motherboard',
                104: 'RAM',
                105: 'Storage',
                106: 'PSU',
                107: 'Mouse',
                108: 'Keyboard',
                109: 'Accessory'
            }

            counts = {}
            for row in results:
                cat_id = row[0]
                count = row[1]

                specific_name = category_map.get(cat_id)

                if specific_name:
                    counts[specific_name] = count

            return counts

        except Exception as e:
            print(f"❌ Error fetching counts: {e}")
            return {}
        finally:
            cursor.close()

    def get_low_stock_products(self):

        cursor = self.db.cursor()
        try:
            query = """
                    SELECT name, stock_quantity
                    FROM products
                    WHERE stock_quantity <= 5
                    ORDER BY stock_quantity ASC \
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            return results

        except Exception as e:
            print(f"❌ Error fetching low stock items: {e}")
            return []
        finally:
            cursor.close()