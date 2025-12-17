from PyQt6 import uic
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout


class Cashierwindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/CashierWindow.ui', self)


