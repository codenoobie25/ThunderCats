import pymysql.cursors

from Model.products_db import ProductsDatabase
from Model.admin_db import AdminDatabase
class Database:
    def __init__(self):
        self.db = self._create_connection()

        self.productdb = ProductsDatabase(self.db)
        self.admindb =  AdminDatabase(self.db)
    def _create_connection(self):
        db = None
        try:
            db = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='thundercatsdb',
                autocommit=True,
            )
            print("✅ Database Connected Successfully!")
            return db
        except pymysql.MySQLError as e:
            print(f"❌ DATABASE ERROR: {e}")
            return None

    def validate_login(self, username, password):
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT Username, Passwords FROM users WHERE Username = %s AND Passwords = %s',
            (username, password,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    def get_user_type(self, Username):
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT Role FROM users WHERE Username = %s',
            (Username,)
        )
        result = cursor.fetchone()
        print(result)
        cursor.close()
        return result
