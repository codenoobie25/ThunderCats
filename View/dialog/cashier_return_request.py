from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class cashier_returnrequest(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UI/RequestReturnItem.ui", self)

        self.cancelButton.clicked.connect(self.close)