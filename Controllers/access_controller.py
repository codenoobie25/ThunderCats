from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox, QHeaderView
from Model.access_db import AccessDatabase
from View.dialog.AddRole import AddRoles


class AccessController:
    def __init__(self, activity_logs_pages, adminWindow_controller):
        self.ui = activity_logs_pages
        self.adminWindow_Controller = adminWindow_controller
        self.db = AccessDatabase(self.adminWindow_Controller.db)

        self.setup_table()

        self.ui.Addrole.clicked.connect(self.open_add_role_dialog)

        self.load_users()

    def setup_table(self):
        table = self.ui.listofAccess

        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "User ID", "Employee ID", "Name", "Username", "Role", "Status", "Actions"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        # Set column widths
        table.setColumnWidth(0, 80)  # User ID
        table.setColumnWidth(1, 100)  # Employee ID
        table.setColumnWidth(2, 200)  # Name
        table.setColumnWidth(3, 150)  # Username
        table.setColumnWidth(4, 120)  # Role
        table.setColumnWidth(5, 100)  # Status
        table.setColumnWidth(6, 200)  # Actions

        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)  # Read-only

    def load_users(self):
        table = self.ui.listofAccess
        table.setRowCount(0)

        users = self.db.get_all_users()

        for row_idx, user_data in enumerate(users):
            user_id, emp_id, username, full_name, role_name, status = user_data

            table.insertRow(row_idx)

            table.setItem(row_idx, 0, QTableWidgetItem(str(user_id)))
            table.setItem(row_idx, 1, QTableWidgetItem(str(emp_id)))
            table.setItem(row_idx, 2, QTableWidgetItem(full_name))
            table.setItem(row_idx, 3, QTableWidgetItem(username))
            table.setItem(row_idx, 4, QTableWidgetItem(role_name))
            table.setItem(row_idx, 5, QTableWidgetItem(status))

            self.add_action_buttons(table, row_idx, user_id, username)

    def add_action_buttons(self, table, row_idx, user_id, username):

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        btn_modify = QPushButton("Modify")
        btn_modify.setStyleSheet("""
            QPushButton {
                background-color: #FFC107; 
                border-radius: 5px; 
                color: black;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
        """)
        btn_modify.clicked.connect(lambda: self.modify_user(user_id))
        layout.addWidget(btn_modify)

        btn_revoke = QPushButton("Revoke")
        btn_revoke.setStyleSheet("""
            QPushButton {
                background-color: #F44336; 
                border-radius: 5px; 
                color: white;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E57373;
            }
        """)
        btn_revoke.clicked.connect(lambda: self.revoke_user(user_id, username))
        layout.addWidget(btn_revoke)

        table.setCellWidget(row_idx, 6, container)

    def open_add_role_dialog(self):

        employees = self.db.get_employees_without_access()

        if not employees:
            QMessageBox.information(None, "No Employees", "All employees already have user accounts!")
            return

        dialog = AddRoles()
        dialog.RoleName.setText("Add User Access")

        dialog.userID.clear()
        for emp_id, full_name, role_name in employees:
            dialog.userID.addItem(f"{emp_id} - {full_name} ({role_name})", emp_id)

        def on_add_clicked():
            emp_id = dialog.userID.currentData()
            username = dialog.username.text().strip()
            password = dialog.password.text().strip()

            if not emp_id:
                QMessageBox.warning(dialog, "Missing Data", "Please select an employee!")
                return

            if not username or not password:
                QMessageBox.warning(dialog, "Missing Data", "Please fill in username and password!")
                return

            try:
                cursor = self.db.db.db.cursor()
                cursor.execute("SELECT roleID FROM employee WHERE employeeID = %s", (emp_id,))
                role_result = cursor.fetchone()
                role_id = role_result[0] if role_result else 1
                cursor.close()

                if self.db.add_user(emp_id, username, password, role_id):
                    QMessageBox.information(dialog, "Success", f"User access granted for {username}!")
                    dialog.accept()
                    self.load_users()
                else:
                    QMessageBox.warning(dialog, "Error", "Failed to add user! Username might already exist.")
            except Exception as e:
                print(f"Error adding user: {e}")
                QMessageBox.critical(dialog, "Error", f"An error occurred: {str(e)}")

        dialog.Addbutton.clicked.connect(on_add_clicked)

        dialog.exec()

    def modify_user(self, user_id):

        from PyQt6.QtWidgets import QInputDialog

        roles = self.db.get_all_roles()
        role_names = [role[1] for role in roles]

        role_name, ok = QInputDialog.getItem(None, "Modify Access", "Select new role:", role_names, 0, False)

        if ok and role_name:
            role_id = next((r[0] for r in roles if r[1] == role_name), None)
            if role_id and self.db.update_user_role(user_id, role_id):
                QMessageBox.information(None, "Success", "User role updated!")
                self.load_users()
            else:
                QMessageBox.warning(None, "Error", "Failed to update role!")

    def revoke_user(self, user_id, username):

        confirm = QMessageBox.question(
            None,
            "Revoke Access",
            f"Are you sure you want to revoke access for '{username}'?\nThis will delete their login credentials.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if self.db.revoke_access(user_id):
                QMessageBox.information(None, "Revoked", "User access has been revoked!")
                self.load_users()
            else:
                QMessageBox.warning(None, "Error", "Failed to revoke access!")