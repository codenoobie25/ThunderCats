import pymysql.cursors

from Model.products_db import ProductsDatabase

class Database:
    def __init__(self):
        self.conn = self._create_connection()
    def __init__(self):
        self.db = self._create_connection()

        self.productdb = ProductsDatabase(self.db)

    def _create_connection(self):
        try:
            conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='thundercatsdb',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✅ Database Connected Successfully!")
            return conn
        except pymysql.MySQLError as e:
            print(f"❌ DATABASE ERROR: {e}")
            return None

    def validate_login(self, username, password):
        """ Checks if user exists. Returns True/False """
        if not self.conn: return False

        cursor = self.conn.cursor()
        # Using %s placeholders for security
        cursor.execute(
            "SELECT * FROM users WHERE Username = %s AND Passwords = %s",
            (username, password)
        )
        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def get_user_role(self, username):

        if not self.conn: return None

        cursor = self.conn.cursor()
        cursor.execute("SELECT Role FROM users WHERE Username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result['Role']
        return None
