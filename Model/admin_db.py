
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

    def get_revenue_details(self):

        cursor = self.db.cursor()
        data = {
            'gross_sale': 0.00,
            'total_transactions': 0,
            'total_items_sold': 0,
            'payment_counts': {}
        }
        try:

            query_sales = "SELECT SUM(total_amount), COUNT(*) FROM sales"
            cursor.execute(query_sales)
            sales_result = cursor.fetchone()

            if sales_result[0] is not None:
                data['gross_sale'] = float(sales_result[0])
            if sales_result[1] is not None:
                data['total_transactions'] = int(sales_result[1])


            query_items = "SELECT SUM(quantity) FROM sale_details"
            cursor.execute(query_items)
            items_result = cursor.fetchone()

            if items_result[0] is not None:
                data['total_items_sold'] = int(items_result[0])

            query_payments = "SELECT payment_method, COUNT(*) FROM sales GROUP BY payment_method"
            cursor.execute(query_payments)
            payment_results = cursor.fetchall()

            for row in payment_results:
                method = row[0]
                count = row[1]
                data['payment_counts'][method] = count

            return data

        except Exception as e:
            print(f"❌ Error fetching revenue details: {e}")
            return data
        finally:
            cursor.close()

    def get_weekly_sales_data(self):
        cursor = self.db.cursor()
        try:
            query = """
                    SELECT DAYNAME(sale_date) as day_name, SUM(total_amount)
                    FROM sales
                    WHERE YEARWEEK(sale_date, 1) = YEARWEEK(CURDATE(), 1)
                    GROUP BY DAYNAME(sale_date) \
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"❌ Error fetching weekly sales: {e}")
            return []
        finally:
            cursor.close()