from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

class CheckoutCashier(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Checkout_cashier.ui", self)

class Receipt(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Receipt.ui", self)