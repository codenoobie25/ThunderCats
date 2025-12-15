from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class SaleReport(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/sale_reportAdmin_page.ui", self)