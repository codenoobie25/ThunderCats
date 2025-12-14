from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class Loginwindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/LoginUI.ui", self)
