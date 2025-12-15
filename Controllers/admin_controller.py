from PyQt6.QtCore import QTimer, QDateTime, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox

from Controllers.dialog_control.TotalproductEX_Controller import TotalproductEXController
from View.dialog.Transaction_Expand import TransactionDialog
from View.dialog.TotalItems_Expand import TotalItemDialog
from View.dialog.TotalRev_expand import TotalRevDialog
from Controllers.access_controller import AccessController
from Controllers.activityLogs_controller import ActivityLogsController
from Controllers.approvalreturn_controller import ApprovalReturnController
from Controllers.employee_controller import EmployeeController
from Controllers.product_controller import ProductController
from Controllers.salereport_controller import SaleReportController
from View.pages.AccessAdmin import AccessAdmin
from View.pages.ActivityLogsAdmin import ActivitylogsAdmin
from View.pages.ReturnApproval import Returnapproval
from View.pages.employee_Admin import EmployeeAdmin
from View.pages.productlist_admin import ProductListAdmin
from View.pages.sale_reportAdmin import SaleReport
from View.dialog.OutStockExpand import OutStockDialog

class Adminwindow:
    # logoutSignal = pyqtSignal()
    def __init__(self, adminwindow, db, application):
        self.page = adminwindow
        self.db = db
        self.application = application
        # self.userID = userID
        # self.usertypr = usertypr

        self.pages = None
        self.setup_pages()

        self.productlist_Controller = ProductController(self.pages[0],self)
        self.salereport_Controller = SaleReportController(self.pages[1],self)
        self.employee_Controller = EmployeeController(self.pages[2],self)
        self.access_Controller = AccessController(self.pages[3],self)
        self.activitylogs_Controller = ActivityLogsController(self.pages[4],self)
        self.approvalreturn_Controller = ApprovalReturnController(self.pages[5],self)

        # self.setup_labels()
        #self.setup_buttons()
        self.set_up_card_button()
        self.setup_navigation()
        self.setup_clock()
        self.setup_logout()
        self.update_total_product()
        self.page.stackedWidget.setCurrentIndex(0)


    def setup_navigation(self):
        print(f"DEBUG: Setting up navigation for {len(self.pages)} pages")

        nav_buttons = {
            self.page.Dashboard2: 0,
            self.page.Productlist: 1,
            self.page.SaleReport: 2,
            self.page.Employee: 3,
            self.page.Access: 4,
            self.page.Returnapprovals:5
        }
        for button,page_index in nav_buttons.items():
            if button:
                 button.clicked.connect(lambda checked, index=page_index:
                                       self.page.stackedWidget.setCurrentIndex(index))
                 print(f"DEBUG: Connected {button.objectName()} -> Index {page_index}")

        print(f"DEBUG: StackedWidget has {self.page.stackedWidget.count()} total pages")

    def setup_logout(self):
        if hasattr(self.page, 'Logoutbtn'):
            self.page.Logoutbtn.clicked.connect(self.confirm_logout)
            print("✓ Logout button connected")

    def confirm_logout(self):
        msg_box = QMessageBox(self.page)
        msg_box.setWindowTitle("Confirm Logout")
        msg_box.setText("Are you sure you want to logout?")

        msg_box.setWindowIcon(QIcon("assets/50x50.png"))

        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        response = msg_box.exec()

        if response == QMessageBox.StandardButton.Yes:
            self.perform_logout()
        else:
            print("User canceled logout")

    def perform_logout(self):
        print("Logging out...")

        if hasattr(self, 'timer'):
            self.timer.stop()

        self.page.close()

        self.application.logout()
    def set_up_card_button(self):
        print("Setting up card expand buttons...")
        print("Connecting card expand buttons...")

        # Connect each button directly to its dialog
        if hasattr(self.page, 'totalrevenue_expand'):
            self.page.totalrevenue_expand.clicked.connect(self.open_total_revenue_dialog)

        if hasattr(self.page, 'totalitems_expand'):
            self.page.totalitems_expand.clicked.connect(self.open_total_items_dialog)

        if hasattr(self.page, 'transaction_expand'):
            self.page.transaction_expand.clicked.connect(self.open_transaction_dialog)

        if hasattr(self.page, 'outstock_expand'):
            self.page.outstock_expand.clicked.connect(self.open_outstock_dialog)

        print("Card buttons connected successfully")


    def open_total_revenue_dialog(self):
        dialog = TotalRevDialog()
        dialog.closeButton.clicked.connect(dialog.close)
        dialog.exec()

    def open_total_items_dialog(self):
        category_counts = self.db.admindb.get_category_counts()
        print("DEBUG Counts:", category_counts)

        dialog = TotalItemDialog()

        self.ex_controller = TotalproductEXController(dialog, category_counts)
        dialog.closeButton.clicked.connect(dialog.close)
        dialog.exec()

    def update_total_product(self):
        counts = self.db.admindb.get_category_counts()

        # 2. Calculate the Total (Sum of all values)
        total_items = sum(counts.values())
        print(f"DEBUG: Total Products Calculated: {total_items}")

        if hasattr(self.page, 'totalProduct'):
            self.page.totalProduct.setText(str(total_items))
        else:
            print("⚠️ Could not find the dashboard label. Check the objectName!")
    def open_transaction_dialog(self):
        dialog = TransactionDialog()
        dialog.closeButton.clicked.connect(dialog.close)
        dialog.exec()

    def open_outstock_dialog(self):
        dialog = OutStockDialog()
        dialog.closeButton.clicked.connect(dialog.close)
        dialog.exec()

    def setup_pages(self):
        self.pages = [
            ProductListAdmin(),
            SaleReport(),
            EmployeeAdmin(),
            AccessAdmin(),
            ActivitylogsAdmin(),
            Returnapproval()
        ]
        for page in self.pages:
            self.page.stackedWidget.addWidget(page)
        # print(f"DEBUG: Added {len(self.pages)} pages. Total pages: {self.page.stackedWidget.count()}")
        # print(f"DEBUG: Index 0 = Dashboard (from UI), Index 1 = {type(self.pages[0]).__name__}")

    def setup_clock(self):
        current = QDateTime.currentDateTime()

        if hasattr(self.page, 'dateEdit'):
                self.page.dateEdit.setDate(current.date())
                self.page.dateEdit.setDisplayFormat("MMMM d, yyyy")
        if hasattr(self.page, 'timeEdit'):
                self.page.timeEdit.setTime(current.time())
                self.page.timeEdit.setDisplayFormat("hh:mm:ss Ap")
            # Create timer to update every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every 1000ms (1 second)

        print("DEBUG: Real-time clock started")

    def update_clock(self):

        current = QDateTime.currentDateTime()

        if hasattr(self.page, 'timeEdit'):
            self.page.timeEdit.setTime(current.time())

        if hasattr(self.page, 'dateEdit'):
            if current.time().hour() == 0 and current.time().minute() == 0:
                self.page.dateEdit.setDate(current.date())



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