class AccessDatabase:
    def __init__(self, db):
        self.db = db

    def get_employees_without_access(self):

        if not self.db: return []
        try:
            cursor = self.db.db.cursor()
            query = """
                SELECT e.employeeID, 
                       CONCAT(e.emp_first_name, ' ', e.emp_last_name) as full_name,
                       r.role_name
                FROM employee e
                LEFT JOIN users u ON e.employeeID = u.employeeID
                LEFT JOIN employee_roles r ON e.roleID = r.roleID
                WHERE u.userID IS NULL
                ORDER BY e.employeeID
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ DB Error (Get Employees Without Access): {e}")
            return []

    def get_all_users(self):

        if not self.db: return []
        try:
            cursor = self.db.db.cursor()
            query = """
                SELECT u.userID,
                       u.employeeID,
                       u.username,
                       CONCAT(e.emp_first_name, ' ', e.emp_last_name) as full_name,
                       r.role_name,
                       u.status
                FROM users u
                JOIN employee e ON u.employeeID = e.employeeID
                JOIN employee_roles r ON u.roleID = r.roleID
                ORDER BY u.userID DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ DB Error (Get All Users): {e}")
            return []

    def add_user(self, employee_id, username, password, role_id):

        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                INSERT INTO users (employeeID, username, password, roleID, status)
                VALUES (%s, %s, %s, %s, 'Active')
            """
            cursor.execute(query, (employee_id, username, password, role_id))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"✗ DB Error (Add User): {e}")
            return False

    def update_user_role(self, user_id, role_id):

        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = "UPDATE users SET roleID = %s WHERE userID = %s"
            cursor.execute(query, (role_id, user_id))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"✗ DB Error (Update User Role): {e}")
            return False

    def revoke_access(self, user_id):

        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = "DELETE FROM users WHERE userID = %s"
            cursor.execute(query, (user_id,))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"✗ DB Error (Revoke Access): {e}")
            return False

    def toggle_user_status(self, user_id):

        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                UPDATE users 
                SET status = CASE 
                    WHEN status = 'Active' THEN 'Inactive'
                    ELSE 'Active'
                END
                WHERE userID = %s
            """
            cursor.execute(query, (user_id,))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"✗ DB Error (Toggle Status): {e}")
            return False

    def get_all_roles(self):

        if not self.db: return []
        try:
            cursor = self.db.db.cursor()
            query = "SELECT roleID, role_name FROM employee_roles"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ DB Error (Get Roles): {e}")
            return []