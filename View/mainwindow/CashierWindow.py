from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from View.pages.InventoryList import inventorylistcashier
from View.dialog.cashier_return_request import cashier_returnrequest
class Cashierwindow(QWidget):
    logoutSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        loadUi('UI/Cashierwindow.ui', self)

        self.inventoryListCashier = inventorylistcashier()
        self.cashierReturnrequest = cashier_returnrequest()

        self.stackedWidget.addWidget(self.inventoryListCashier)

        self.ReturnRequestButton.clicked.connect(self.cashier_returnRequest)

        self.cashiernavigation()

        self.Logout.clicked.connect(self.cashier_logout)

    def cashiernavigation(self):

            self.Register.clicked.connect(lambda: self.switch_to_register())
            self.InventoryList.clicked.connect(lambda: self.switch_to_inventory_list())

    def switch_to_register(self):
            # print("Switching to Dashboard (Index 0)")
            self.stackedWidget.setCurrentIndex(0)

    def switch_to_inventory_list(self):
            self.stackedWidget.setCurrentWidget(self.inventoryListCashier)

    def cashier_returnRequest(self):
            cashierReturnrequest = cashier_returnrequest()
            cashierReturnrequest.exec()
    def cashier_logout(self):
        self.logoutSignal.emit()
        self.close()