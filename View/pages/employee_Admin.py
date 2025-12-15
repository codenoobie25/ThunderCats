from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from View.dialog.EmployeeAdd import addemployeeDialog
class EmployeeAdmin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/EmployeeAdmin_page.ui", self)


