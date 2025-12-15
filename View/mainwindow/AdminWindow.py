from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class AdminWindowUI(QWidget):
    def  __init__(self):
        super().__init__()
        uic.loadUi("UI/AdminUI.ui", self)
        self.setWindowTitle("ThunderCats Admin Dashboard")