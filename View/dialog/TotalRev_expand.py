from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class TotalRevDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/totalrev_expand.ui", self)

        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.closeButton.clicked.connect(self.close)

