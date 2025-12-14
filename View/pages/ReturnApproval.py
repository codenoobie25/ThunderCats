from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


class Returnapproval(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/ReturnItems_page.ui", self)