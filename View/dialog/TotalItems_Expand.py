from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class TotalItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Totalitems_expand.ui", self)

        self.closeButton.clicked.connect(self.close)