import pymysql
class SaleReportDatabase:
    def __init__(self,db):
        self.db = db

    def fetch_revenue_by_category(self, start_date, end_date):

        if not self.db:
            return []
        try:
            cursor = self.db.cursor(pymysql.cursors.DictCursor)

            # This query joins Sales -> Details -> Products -> Categories
            # It sums up the subtotal for each category automatically.
            query = "SELECT c.categoryName as Category, SUM(sd.subtotal) as Revenue FROM sales s JOIN sale_details sd ON s.sale_id = sd.sale_id JOIN products p ON sd.product_id = p.product_id LEFT JOIN category c ON p.categoryID = c.categoryID WHERE s.sale_date BETWEEN %s AND %s GROUP BY c.categoryName ORDER BY Revenue DESC"

            cursor.execute(query, (start_date,end_date))
            result = cursor.fetchall()
            return result
        except pymysql.MySQLError as e:
            print(f"❌ Error fetching category revenue: {e}")
            return []

    def fetch_top_products(self, start_date, end_date):

            if not self.db:
                return []

            try:
                cursor = self.db.cursor(pymysql.cursors.DictCursor)
                query = "SELECT p.name as product_name, SUM(sd.quantity) as quantity FROM sales s JOIN sale_details sd ON s.sale_id = sd.sale_id JOIN products p ON sd.product_id = p.product_id WHERE s.sale_date BETWEEN %s AND %s GROUP BY p.name ORDER BY quantity DESC LIMIT 5"
                cursor.execute(query, (start_date, end_date))
                return cursor.fetchall()
            except pymysql.MySQLError as e:
                print(f"Error fetching top products: {e}")
                return []

    def fetch_summary_stats(self, start_date, end_date):
        # Default fallback
        stats = {'total_sales': 0.0, 'avg_ticket': 0.0, 'top_category': 'None'}

        if not self.db:
            return stats
        try:
            cursor = self.db.cursor(pymysql.cursors.DictCursor)

            query_totals = "SELECT COALESCE(SUM(total_amount), 0) as total_sales, COALESCE(AVG(total_amount), 0) as avg_ticket FROM sales WHERE sale_date BETWEEN %s AND %s"
            cursor.execute(query_totals, (start_date, end_date))
            result_totals = cursor.fetchone()

            if result_totals:
                stats['total_sales'] = float(result_totals['total_sales'])
                stats['avg_ticket'] = float(result_totals['avg_ticket'])

            query_top_cat = "SELECT c.categoryName FROM sales s JOIN sale_details sd ON s.sale_id = sd.sale_id JOIN products p ON sd.product_id = p.product_id LEFT JOIN category c ON p.categoryID = c.categoryID WHERE s.sale_date BETWEEN %s AND %s GROUP BY c.categoryName ORDER BY SUM(sd.subtotal) DESC LIMIT 1"
            cursor.execute(query_top_cat, (start_date, end_date))
            result_cat = cursor.fetchone()

            if result_cat and 'categoryName' in result_cat:
                stats['top_category'] = result_cat['categoryName']
            else:
                stats['top_category'] = "None"

            return stats

        except Exception as e:
            # Changed to generic Exception so it catches KeyErrors too
            print(f"❌ Error fetching summary stats: {e}")
            return stats

    def add_generated_report(self, report_name, file_path, report_type):

        if not self.db: return False
        try:
            cursor = self.db.cursor()
            query = "INSERT INTO generated_reports (report_name, file_path, report_type) VALUES (%s, %s, %s)"
            cursor.execute(query, (report_name, file_path, report_type))
            return True
        except Exception as e:
            print(f"❌ Error saving report record: {e}")
            return False

    def fetch_all_reports(self):

        if not self.db: return []
        try:
            cursor = self.db.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT * FROM generated_reports ORDER BY date_created DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching report history: {e}")
            return []

    def fetch_sales_list(self, start_date, end_date):
        if not self.db: return []
        try:
            cursor = self.db.cursor()

            query = "SELECT s.sale_id, p.name, c.categoryName, (sd.subtotal / sd.quantity) as price, s.sale_date, sd.subtotal, s.payment_method FROM sales s JOIN sale_details sd ON s.sale_id = sd.sale_id JOIN products p ON sd.product_id = p.product_id LEFT JOIN category c ON p.categoryID = c.categoryID WHERE s.sale_date BETWEEN %s AND %s ORDER BY s.sale_date DESC"
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales list: {e}")
            return []

    def fetch_product_sales_list(self, start_date, end_date):
        if not self.db: return []
        try:
            cursor = self.db.cursor()

            query = "SELECT p.name, c.categoryName, SUM(sd.quantity), SUM(sd.subtotal) FROM sale_details sd JOIN sales s ON sd.sale_id = s.sale_id JOIN products p ON sd.product_id = p.product_id LEFT JOIN category c ON p.categoryID = c.categoryID WHERE s.sale_date BETWEEN %s AND %s GROUP BY p.name ORDER BY SUM(sd.subtotal) DESC"
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching product list: {e}")
            return []