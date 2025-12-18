import pymysql.cursors
from Model.access_db import AccessDatabase
from Model.cashier_db import CashierDatabase
from Model.employee_db import EmployeeDatabase
from Model.products_db import ProductsDatabase
from Model.admin_db import AdminDatabase
from Model.salereport_db import SaleReportDatabase
from Model.sales import SalesDatabase


class Database:
    def __init__(self):
        self.db = self._create_connection()

        self.productdb = ProductsDatabase(self.db)
        self.admindb =  AdminDatabase(self.db)
        self.salereportdb = SaleReportDatabase(self.db)
        self.employeedb = EmployeeDatabase(self.db)
        self.accessdb = AccessDatabase(self.db)
        self.cashierdb = CashierDatabase(self.db)
        self.salesdb = SalesDatabase(self.db)
        self.admindb = AdminDatabase(self.db)
    def _create_connection(self):
        db = None
        try:
            db = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='thundercatsdb',
                autocommit=False,
            )
            print("✅ Database Connected Successfully!")
            return db
        except pymysql.MySQLError as e:
            print(f"❌ DATABASE ERROR: {e}")
            return None

    def validate_login(self, username, password):
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT username, password FROM users WHERE username = %s AND password = %s',
            (username, password,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_user_type(self, Username):
        cursor = self.db.cursor()
        cursor.execute(
            '''
            SELECT r.role_name
            FROM users u
                     JOIN employee_roles r ON u.roleID = r.roleID
            WHERE u.username = %s
            ''',
            (Username,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result