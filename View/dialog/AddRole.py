from PyQt6.QtWidgets import QWidget, QDialog
from PyQt6.uic import loadUi

class AddRoles(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UI/AddRole.ui", self)


        self.Cancelbutton.clicked.connect(self.close)