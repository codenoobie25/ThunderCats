from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class OutStockDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Outstock_expand.ui", self)


