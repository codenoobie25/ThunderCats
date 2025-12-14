from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/AdminUI.ui", self)
        self.setWindowTitle("ThunderCats Admin Dashboard")