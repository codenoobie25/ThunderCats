
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class AddProduct(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UI/Add_product.ui", self)

        #elf.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
