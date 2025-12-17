class EmployeeDatabase:
    def __init__(self, db):
        self.db = db

    def get_all_employees(self):

        if not self.db: return []
        try:
            cursor = self.db.db.cursor()
            query = """
                    SELECT e.employeeID, \
                           e.emp_first_name, \
                           e.emp_last_name, \
                           r.role_name, \
                           e.status, \
                           e.emp_email, \
                           e.date_hired, \
                           e.emp_phone, \
                           e.street_address, \
                           e.city, \
                           e.province, \
                           e.roleID
                    FROM employee e
                             LEFT JOIN employee_roles r ON e.roleID = r.roleID
                    ORDER BY e.employeeID DESC \
                    """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ DB Error (Get Employees): {e}")
            return []

    def add_employee(self, first_name, last_name, role_id, email, date_hired, phone, status, street, city, province):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                INSERT INTO employee 
                (emp_first_name, emp_last_name, roleID, emp_email, date_hired, emp_phone, status, street_address, city, province)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, role_id, email, date_hired, phone, status, street, city, province))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error (Add Employee): {e}")
            return False

    def update_employee(self, emp_id, first_name, last_name, role_id, email, date_hired, phone, status, street, city, province):

        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = """
                UPDATE employee 
                SET emp_first_name=%s, emp_last_name=%s, roleID=%s, emp_email=%s, 
                    date_hired=%s, emp_phone=%s, status=%s, street_address=%s, city=%s, province=%s
                WHERE employeeID=%s
            """
            cursor.execute(query, (first_name, last_name, role_id, email, date_hired, phone, status, street, city, province, emp_id))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error (Update Employee): {e}")
            return False

    def delete_employee(self, emp_id):
        if not self.db: return False
        try:
            cursor = self.db.db.cursor()
            query = "DELETE FROM employee WHERE employeeID = %s"
            cursor.execute(query, (emp_id,))
            self.db.db.commit()
            return True
        except Exception as e:
            print(f"❌ DB Error (Delete Employee): {e}")
            return False

    def get_all_roles(self):
        if not self.db: return []
        try:
            cursor = self.db.db.cursor()
            query = "SELECT roleID, role_name FROM employee_roles"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ DB Error (Get Roles): {e}")
            return []