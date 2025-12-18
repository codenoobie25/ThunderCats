from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox
import matplotlib

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout

from Controllers.dialog_control.OutofStock_LowStockEx_Controller import OutofStockLowStockExCntroller
from Controllers.dialog_control.TotalRevenueEX_Controller import TotalRevenueEXController
from Controllers.dialog_control.TotalproductEX_Controller import TotalproductEXController
from View.dialog.TotalItems_Expand import TotalItemDialog
from View.dialog.TotalRev_expand import TotalRevDialog
from Controllers.access_controller import AccessController
from Controllers.employee_controller import EmployeeController
from Controllers.product_controller import ProductController
from Controllers.salereport_controller import SaleReportController
from View.pages.AccessAdmin import AccessAdmin
from View.pages.ReturnApproval import Returnapproval
from View.pages.employee_Admin import EmployeeAdmin
from View.pages.productlist_admin import ProductListAdmin
from View.pages.sale_reportAdmin import SaleReport
from View.dialog.OutStockExpand import OutStockDialog

class Adminwindow:
    def __init__(self, adminwindow, db, application):
        self.page = adminwindow
        self.db = db
        self.application = application

        self.pages = None
        self.setup_pages()

        self.productlist_Controller = ProductController(self.pages[0],self)
        self.salereport_Controller = SaleReportController(self.pages[1],self)
        self.employee_Controller = EmployeeController(self.pages[2],self)
        self.access_Controller = AccessController(self.pages[3],self)

        self.set_up_card_button()
        self.setup_navigation()
        self.setup_clock()
        self.setup_logout()
        self.update_total_product()
        self.update_out_of_stock_total()
        self.update_revenue_dashboard()
        self.setup_weekly_sales_chart()
        self.page.stackedWidget.setCurrentIndex(0)

    def setup_navigation(self):
        print(f"DEBUG: Setting up navigation for {len(self.pages)} pages")

        nav_buttons = {
            self.page.Dashboard2: 0,
            self.page.Productlist: 1,
            self.page.SaleReport: 2,
            self.page.Employee: 3,
            self.page.Access: 4
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

        if hasattr(self.page, 'totalrevenue_expand'):
            self.page.totalrevenue_expand.clicked.connect(self.open_total_revenue_dialog)

        if hasattr(self.page, 'totalitems_expand'):
            self.page.totalitems_expand.clicked.connect(self.open_total_items_dialog)

        if hasattr(self.page, 'outstock_expand'):
            self.page.outstock_expand.clicked.connect(self.open_outstock_dialog)


    def open_total_revenue_dialog(self):
        revenue_data = self.db.admindb.get_revenue_details()
        print("DEBUG Revenue Data:", revenue_data)

        dialog = TotalRevDialog()

        self.rev_controller = TotalRevenueEXController(dialog, revenue_data)

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


    def update_out_of_stock_total(self):

        low_stock_list = self.db.admindb.get_low_stock_products()

        total_alerts = len(low_stock_list)
        print(f"DEBUG: Total Low/Out Stock Items: {total_alerts}")

        if hasattr(self.page, 'Counts'):
            self.page.Counts.setText(str(total_alerts))
        else:
            print("⚠️ Could not find 'Counts' label on dashboard.")

    def open_outstock_dialog(self):
        low_stock_data = self.db.admindb.get_low_stock_products()
        print(f"DEBUG: Found {len(low_stock_data)} low stock items")

        dialog = OutStockDialog()

        self.os_controller = OutofStockLowStockExCntroller(dialog, low_stock_data)

        dialog.closeButton.clicked.connect(dialog.close)
        dialog.exec()

    def setup_pages(self):
        self.pages = [
            ProductListAdmin(),
            SaleReport(),
            EmployeeAdmin(),
            AccessAdmin(),
            Returnapproval()
        ]
        for page in self.pages:
            self.page.stackedWidget.addWidget(page)


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

    def update_revenue_dashboard(self):

        data = self.db.admindb.get_revenue_details()

        gross_sale = data.get('gross_sale', 0.00)

        formatted_revenue = "{:,.2f}".format(gross_sale)
        print(f"DEBUG: Total Revenue for Dashboard: {formatted_revenue}")

        if hasattr(self.page, 'totalRev'):
            self.page.totalRev.setText(formatted_revenue)

    def setup_weekly_sales_chart(self):
        raw_data = self.db.admindb.get_weekly_sales_data()

        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        sales_map = {day: 0.0 for day in days_order}

        if raw_data:
            for row in raw_data:
                day_name = row[0]
                total = float(row[1])
                if day_name in sales_map:
                    sales_map[day_name] = total

        x_days = days_order
        y_amounts = [sales_map[day] for day in days_order]

        fig, ax = plt.subplots(figsize=(5, 3))  # Size doesn't matter much, layout handles it

        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        ax.plot(x_days, y_amounts, marker='o', color='#FFD700', linewidth=2)

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')

        # Add labels (Optional)
        ax.set_ylabel('Sales', color='white')

        target_widget = self.page.WeeklyRevChart

        if target_widget.layout() is None:
            layout = QVBoxLayout(target_widget)
            target_widget.setLayout(layout)
        else:
            layout = target_widget.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

        print("✅ Weekly Sales Chart Updated")