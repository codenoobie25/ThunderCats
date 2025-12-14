from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from View.dialog.EmployeeAdd import addemployeeDialog
class EmployeeAdmin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/EmployeeAdmin_page.ui", self)
        print("Employee page is loaded ")

        self.addingEmployee = addemployeeDialog()

        self.addemployee.clicked.connect(self.openEmployeeAdd)

    def openEmployeeAdd(self):
        addingEmployee = addemployeeDialog()
        addingEmployee.exec()
