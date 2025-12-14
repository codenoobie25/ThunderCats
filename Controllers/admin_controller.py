from PyQt6.QtCore import QTimer, QDateTime, pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from Model.database import Database
from View.mainwindow.AdminWindow import AdminWindow
from View.pages.productlist_admin import ProductListAdmin
from View.pages.sale_reportAdmin import SaleReportAdmin
from View.pages.employee_Admin import EmployeeAdmin
from View.pages.AccessAdmin import AccessAdmin
from View.dialog.TotalRev_expand import TotalRevDialog
from View.dialog.TotalItems_Expand import TotalItemDialog
from View.dialog.Transaction_Expand import TransactionDialog
from View.dialog.OutStockExpand import OutStockDialog
from View.pages.ActivityLogsAdmin import ActivitylogsAdmin
from View.pages.ReturnApproval import Returnapproval

class Adminwindow(QWidget):
    # logoutSignal = pyqtSignal()
    def __init__(self,adminwindow,db, application,lastname,firstname):
        self.page = adminwindow
        self.db = db
        self.application = application
        self.lastname = lastname
        self.firstname = firstname

        self.pages = None
        self.setup_pages()
    def setup_pages(self):
        self.pages =[
        ProductListAdmin(),
        SaleReportAdmin()
        ]
        for page in self.pages:
            self.page.stackedWidget.addWidget(page)



    #     # Dashboard Pages
    #     self.page_productlist = ProductListAdmin()
    #     self.page_salereport = SaleReportAdmin()
    #     self.page_employee = EmployeeAdmin()
    #     self.page_access = AccessAdmin()
    #     self.page_activities = ActivitylogsAdmin()
    #     self.page_returnapproval = Returnapproval()
    #
    #     self.expand_totalrev = TotalRevDialog()
    #     self.expand_totalitems = TotalItemDialog()
    #     self.expand_transaction = TransactionDialog()
    #     self.expand_outstock = OutStockDialog()
    #
    #     self.stackedWidget.addWidget(self.page_productlist)
    #     self.stackedWidget.addWidget(self.page_salereport)
    #     self.stackedWidget.addWidget(self.page_employee)
    #     self.stackedWidget.addWidget(self.page_access)
    #     self.stackedWidget.addWidget(self.page_activities)
    #     self.stackedWidget.addWidget(self.page_returnapproval)
    #
    #
    #     # four card expand functions
    #     self.totalrevenue_expand.clicked.connect(self.openTotalrev)
    #     self.transaction_expand.clicked.connect(self.openTransaction)
    #     self.totalitems_expand.clicked.connect(self.openTotalitems)
    #     self.outstock_expand.clicked.connect(self.openOutstock)
    #
    #     self.setup_navigation()
    #
    #     # 2. Timer/Clock Setup
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.update_clock)
    #     self.timer.start(1000)
    #     self.update_clock()
    #
    #     # 3. Connect Logout
    #     self.Logoutbtn.clicked.connect(self.admin_logout)
    #
    # def setup_navigation(self):
    #
    #     self.Dashboard2.clicked.connect(lambda: self.switch_to_dashboard())
    #     self.Productlist.clicked.connect(lambda: self.switch_to_product_page())
    #     self.SaleReport.clicked.connect(lambda: self.switch_to_sale_report())
    #     self.Employee.clicked.connect(lambda: self.switch_to_employee())
    #     self.Access.clicked.connect(lambda: self.switch_to_access())
    #     self.Activitylogs.clicked.connect(lambda: self.switch_to_activities())
    #     self.Returnapprovals.clicked.connect(lambda: self.switch_to_returnapproval())
    #
    # def openTotalrev(self):
    #     expand_totalrev = TotalRevDialog()
    #     expand_totalrev.exec()
    # def openTotalitems(self):
    #     expand_totalitems = TotalItemDialog()
    #     expand_totalitems.exec()
    # def openTransaction(self):
    #     expand_transaction = TransactionDialog()
    #     expand_transaction.exec()
    # def openOutstock(self):
    #     expand_outstock = OutStockDialog()
    #     expand_outstock.exec()
    #
    # def switch_to_dashboard(self):
    #     #print("Switching to Dashboard (Index 0)")
    #     self.stackedWidget.setCurrentIndex(0)
    # def switch_to_product_page(self):
    #     self.stackedWidget.setCurrentWidget(self.page_productlist)
    # def switch_to_sale_report(self):
    #     self.stackedWidget.setCurrentWidget(self.page_salereport)
    # def switch_to_employee(self):
    #     self.stackedWidget.setCurrentWidget(self.page_employee)
    # def switch_to_access(self):
    #     self.stackedWidget.setCurrentWidget(self.page_access)
    # def switch_to_activities(self):
    #     self.stackedWidget.setCurrentWidget(self.page_activities)
    # def switch_to_returnapproval(self):
    #     self.stackedWidget.setCurrentWidget(self.page_returnapproval)
    # def update_clock(self):
    #     now = QDateTime.currentDateTime()
    #     if hasattr(self, 'dateEdit'):
    #         self.dateEdit.setDate(now.date())
    #     if hasattr(self, 'timeEdit'):
    #         self.timeEdit.setTime(now.time())
    #
    # def admin_logout(self):
    #     self.logoutSignal.emit()
    #     self.close()