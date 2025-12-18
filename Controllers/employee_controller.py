from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox, QDialog
from PyQt6.QtCore import Qt, QDate

from Model.employee_db import EmployeeDatabase
from View.dialog.EmployeeAdd import addemployeeDialog


class EmployeeController:
    def __init__(self, main_window_ui, adminController):
        self.ui = main_window_ui
        self.adminController = adminController
        self.db = EmployeeDatabase(self.adminController.db)
        self.current_edit_id = None

        self.load_employees()
        self.update_dashboard_counts()

        self.ui.addemployee.clicked.connect(self.open_add_dialog)
        self.ui.search_bar.textChanged.connect(self.filter_table)

    def load_employees(self):

        data = self.db.get_all_employees()

        table = self.ui.EmployeeList
        table.setRowCount(0)

        for row_idx, row_data in enumerate(data):
            table.insertRow(row_idx)


            emp_id = str(row_data[0])
            full_name = f"{row_data[1]} {row_data[2]}"
            role_name = str(row_data[3])
            status = row_data[4]

            table.setItem(row_idx, 0, QTableWidgetItem(emp_id))
            table.setItem(row_idx, 1, QTableWidgetItem(full_name))
            table.setItem(row_idx, 2, QTableWidgetItem(role_name))
            table.setItem(row_idx, 3, QTableWidgetItem(status))

            self.add_action_buttons(table, row_idx, row_data)

        self.update_dashboard_counts()

    def add_action_buttons(self, table, row_idx, row_data):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        btn_edit = QPushButton("Edit")
        btn_edit.setStyleSheet("background-color: #FFC107; border-radius: 5px; color: black;")
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(row_data))

        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background-color: #F44336; border-radius: 5px; color: white;")
        btn_delete.clicked.connect(lambda: self.delete_employee(row_data[0]))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        table.setCellWidget(row_idx, 4, container)

    def populate_role_combobox(self, combo_box):
            combo_box.clear()
            roles = self.db.get_all_roles()
            print(f"DEBUG: Retrieved {len(roles)} roles: {roles}")

            for role_id, role_name in roles:
                combo_box.addItem(role_name, role_id)

    def open_add_dialog(self):
        try:
            self.dialog = addemployeeDialog()
            self.dialog.Header.setText("Add New Employee")
            self.populate_role_combobox(self.dialog.Rolebox)
            self.dialog.datejoin.setDate(QDate.currentDate())
            self.dialog.addButton.clicked.connect(self.save_employee_from_dialog)
            self.dialog.cancelButton.clicked.connect(self.dialog.close)

            print("DEBUG: About to exec()")
            result = self.dialog.exec()
            print(f"DEBUG: Dialog returned: {result}")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

    def open_edit_dialog(self, row_data):
        try:
            print(f"DEBUG: Starting open_edit_dialog with row_data: {row_data}")
            self.current_edit_id = row_data[0]

            self.dialog = addemployeeDialog()

            self.dialog.setWindowTitle("Edit Employee")
            self.dialog.Header.setText("Edit Employee")
            self.dialog.addButton.setText("Save Changes")

            self.populate_role_combobox(self.dialog.Rolebox)

            self.dialog.firstName.setText(row_data[1])
            self.dialog.lastName.setText(row_data[2])
            self.dialog.Emailadd.setText(row_data[5])
            self.dialog.Phonenumber.setText(row_data[7])
            self.dialog.streetAdd.setText(row_data[8])
            self.dialog.city.setText(row_data[9])
            self.dialog.province.setText(row_data[10])

            role_id_from_db = row_data[11]
            print(f"DEBUG: role_id_from_db = {role_id_from_db}")
            idx = self.dialog.Rolebox.findData(role_id_from_db)
            print(f"DEBUG: Role index found: {idx}")
            if idx >= 0:
                self.dialog.Rolebox.setCurrentIndex(idx)

            status_text = row_data[4]
            print(f"DEBUG: status_text = {status_text}")
            status_idx = self.dialog.empstatus.findText(status_text)
            print(f"DEBUG: Status index found: {status_idx}")
            if status_idx >= 0:
                self.dialog.empstatus.setCurrentIndex(status_idx)

            db_date_str = str(row_data[6])
            print(f"DEBUG: db_date_str = {db_date_str}")
            qdate = QDate.fromString(db_date_str, "yyyy-MM-dd")
            print(f"DEBUG: qdate = {qdate}")
            self.dialog.datejoin.setDate(qdate)

            self.dialog.addButton.clicked.connect(self.save_employee_from_dialog)
            self.dialog.cancelButton.clicked.connect(self.dialog.close)

            self.dialog.exec()

        except Exception as e:
            print(f"ERROR in open_edit_dialog: {e}")
            import traceback
            traceback.print_exc()

    def save_employee_from_dialog(self):
        print("DEBUG: Starting save_employee_from_dialog")

        try:
            f_name = self.dialog.firstName.text()
            l_name = self.dialog.lastName.text()
            email = self.dialog.Emailadd.text()
            phone = self.dialog.Phonenumber.text()
            street = self.dialog.streetAdd.text()
            city = self.dialog.city.text()
            prov = self.dialog.province.text()

            print("DEBUG: Getting date")
            date_hired = self.dialog.datejoin.date().toString("yyyy-MM-dd")

            print("DEBUG: Getting role_id")
            role_id = self.dialog.Rolebox.currentData()
            print(f"DEBUG: role_id = {role_id}")

            print("DEBUG: Getting status")
            status = self.dialog.empstatus.currentText()
            print(f"DEBUG: status = {status}")

            # Validation
            if not f_name or not l_name:
                print("DEBUG: Missing name")
                QMessageBox.warning(self.dialog, "Missing Data", "Please fill in First Name and Last Name.")
                return

            if role_id is None:
                print("DEBUG: Missing role")
                QMessageBox.warning(self.dialog, "Missing Data", "Please select a Role.")
                return

            print("DEBUG: Validation passed")

            if self.current_edit_id is None:
                # Add new employee
                confirm = QMessageBox.question(self.dialog, "Confirm", "Add new employee?",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if confirm == QMessageBox.StandardButton.Yes:
                    print("DEBUG: Calling add_employee")
                    success = self.db.add_employee(
                        f_name, l_name, role_id, email, date_hired,
                        phone, status, street, city, prov
                    )
                    print(f"DEBUG: add_employee returned {success}")
                    if success:
                        QMessageBox.information(self.dialog, "Success", "Employee Added!")
                        self.dialog.close()
                        self.load_employees()
                    else:
                        QMessageBox.warning(self.dialog, "Error", "Failed to add to Database.")
            else:
                # Update existing employee
                confirm = QMessageBox.question(self.dialog, "Confirm", "Save changes?",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if confirm == QMessageBox.StandardButton.Yes:
                    print("DEBUG: Calling update_employee")
                    success = self.db.update_employee(
                        self.current_edit_id,
                        f_name, l_name, role_id, email, date_hired,
                        phone, status, street, city, prov
                    )
                    print(f"DEBUG: update_employee returned {success}")
                    if success:
                        QMessageBox.information(self.dialog, "Success", "Employee Updated!")
                        self.dialog.close()
                        self.load_employees()
                    else:
                        QMessageBox.warning(self.dialog, "Error", "Failed to update Database.")

        except Exception as e:
            print(f"ERROR in save_employee_from_dialog: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.dialog, "Error", f"An error occurred: {str(e)}")

    def delete_employee(self, emp_id):
        confirm = QMessageBox.warning(None, "Delete", "Are you sure? This cannot be undone.",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            if self.db.delete_employee(emp_id):
                QMessageBox.information(None, "Deleted", "Employee record deleted.")
                self.load_employees()
            else:
                QMessageBox.warning(None, "Error", "Could not delete employee.")

    def filter_table(self):
        search_text = self.ui.search_bar.text().lower()
        table = self.ui.EmployeeList

        for row in range(table.rowCount()):
            id_txt = table.item(row, 0).text().lower()
            name_txt = table.item(row, 1).text().lower()

            if search_text in id_txt or search_text in name_txt:
                table.setRowHidden(row, False)
            else:
                table.setRowHidden(row, True)

    def update_dashboard_counts(self):
        employees = self.db.get_all_employees()
        total = len(employees)
        active = sum(1 for e in employees if e[4].lower() == 'active')
        deactive = total - active

        self.ui.numberofEmployee.setText(str(total))
        self.ui.numberofActive.setText(str(active))
        self.ui.numberofdeactivatedEmployee.setText(str(deactive))