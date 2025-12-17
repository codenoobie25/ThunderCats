from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class addemployeeDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/AddEmployee.ui", self)
