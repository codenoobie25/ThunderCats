from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class ProductListAdmin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/ProductlistAdmin_page.ui", self)
        print("Product list page is loaded ")
