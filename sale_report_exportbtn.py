from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class Sale_Report_Exportbtn(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/sale_report_exportbtn.ui", self)
        print("Sale report page is loaded ")