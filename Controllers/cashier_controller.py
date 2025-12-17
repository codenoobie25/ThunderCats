from PyQt6.QtCore import QDateTime, QTimer, Qt
from PyQt6.QtWidgets import (
    QMessageBox, QWidget, QGridLayout, QVBoxLayout,
)
from Controllers.dialog_control.checkout_controller import CheckoutCashierController
from View.dialog.chechoutWidget import ProductCardWidget, CartItemWidget
from View.dialog.checkout_cashierUI import CheckoutCashier

class CashierController:


    def __init__(self, cashierwindow, db, application):
        self.page = cashierwindow
        self.db = db
        self.application = application

        self.cart_items = {}
        self.all_products_data = []
        self.all_categories = []  # Store categories
        self.tax_rate = 0.08

        self.setup_clock()
        self.setup_logout()
        self.init_ui_areas()

        # Load data and setup filters
        self.fetch_categories()
        self.fetch_and_store_products()
        self.setup_category_filter()
        self.display_products()

        # Connect search
        if hasattr(self.page, 'SearchItem'):
            self.page.SearchItem.textChanged.connect(self.display_products)

        if hasattr(self.page, 'checkoutButton'):  # Use your actual button name
            self.page.checkoutButton.clicked.connect(self.open_checkout_dialog)

    def init_ui_areas(self):
        """Initialize the product grid and cart scroll areas"""
        if hasattr(self.page, 'scrollArea_products'):
            self.inv_container = QWidget()
            self.inv_layout = QGridLayout(self.inv_container)
            self.inv_layout.setSpacing(15)
            self.inv_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.page.scrollArea_products.setWidget(self.inv_container)
            self.page.scrollArea_products.setWidgetResizable(True)

        if hasattr(self.page, 'scrollArea_cart'):
            self.cart_container = QWidget()
            self.cart_layout = QVBoxLayout(self.cart_container)
            self.cart_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.cart_layout.setSpacing(10)
            self.page.scrollArea_cart.setWidget(self.cart_container)
            self.page.scrollArea_cart.setWidgetResizable(True)

    def fetch_categories(self):
        """Load all categories from database"""
        try:
            self.all_categories = self.db.cashierdb.get_all_categories()
        except Exception as e:
            print(f"Error fetching categories: {e}")
            self.all_categories = []

    def setup_category_filter(self):
        """Populate category filter combobox"""
        if not hasattr(self.page, 'categoryfilter'):
            return

        self.page.categoryfilter.clear()
        self.page.categoryfilter.addItem("All Categories", None)

        for cat_id, cat_name in self.all_categories:
            self.page.categoryfilter.addItem(cat_name, cat_id)

        self.page.categoryfilter.currentIndexChanged.connect(self.display_products)

    def fetch_and_store_products(self):
        """Fetch all products from database once"""
        try:
            self.all_products_data = self.db.cashierdb.get_available_products()
        except Exception as e:
            print(f"Error fetching products: {e}")
            self.all_products_data = []

    def display_products(self):
        """Display filtered products in grid layout"""
        # Clear existing grid
        while self.inv_layout.count():
            child = self.inv_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

            # Get filters
        search_text = ""
        if hasattr(self.page, 'SearchItem'):
            search_text = self.page.SearchItem.text().lower().strip()

        selected_category = None
        if hasattr(self.page, 'categoryfilter'):
            selected_category = self.page.categoryfilter.currentData()

        # Display matching products
        row, col = 0, 0
        max_cols = 3

        for prod in self.all_products_data:
            p_id = prod[0]
            name = prod[1]
            price = prod[2]
            stock = prod[3]
            prod_category = prod[4] if len(prod) > 4 else None  # Get categoryID

            if search_text and search_text not in name.lower():
                continue

            if selected_category is not None and prod_category != selected_category:
                continue

            # Create and add product card
            card = ProductCardWidget(p_id, name, float(price))
            card.clicked.connect(self.add_to_cart)

            self.inv_layout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def add_to_cart(self, product_id):
        if product_id in self.cart_items:
            self.cart_items[product_id].increase_qty()
        else:
            target = next((p for p in self.all_products_data if p[0] == product_id), None)

            if target:
                p_id, name, price, stock = target[:4]  # Get first 4 elements safely
                item_widget = CartItemWidget(p_id, name, float(price))
                item_widget.qty_changed.connect(self.calculate_totals)
                item_widget.item_removed.connect(self.remove_from_cart)

                self.cart_layout.addWidget(item_widget)
                self.cart_items[product_id] = item_widget

        self.calculate_totals()

    def remove_from_cart(self, product_id):

        if product_id in self.cart_items:
            widget = self.cart_items[product_id]
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
            del self.cart_items[product_id]
            self.calculate_totals()

    def calculate_totals(self):

        subtotal = sum(item.get_subtotal() for item in self.cart_items.values())
        tax = subtotal * self.tax_rate
        total = subtotal + tax

        if hasattr(self.page, 'subTotal'):
            self.page.subTotal.setText(f"₱ {subtotal:,.2f}")
        if hasattr(self.page, 'Tax'):
            self.page.Tax.setText(f"₱ {tax:,.2f}")
        if hasattr(self.page, 'Totals'):
            self.page.Totals.setText(f"₱ {total:,.2f}")

    def open_checkout_dialog(self):
        try:
            if not self.cart_items:
                QMessageBox.warning(self.page, "Empty Cart", "Please add items to cart before checking out.")
                return

            cart_list = []
            for product_id, cart_widget in self.cart_items.items():
                product = next((p for p in self.all_products_data if p[0] == product_id), None)
                if product:
                    cart_list.append({
                        'product_id': product_id,
                        'product_name': product[1],
                        'quantity': cart_widget.quantity,
                        'unit_price': cart_widget.unit_price,
                        'subtotal': cart_widget.get_subtotal()
                    })


            checkout_dialog = CheckoutCashier()

            self.checkout_controller = CheckoutCashierController(
                checkout_dialog,
                self.db.salesdb,
                cart_list,
                self
            )

            checkout_dialog.exec()

        except Exception as e:
            print(f"ERROR in open_checkout_dialog: {e}")
            import traceback
            traceback.print_exc()

    # def get_current_user_id(self):
    #     return 1

    def clear_cart_after_checkout(self):
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()

        self.cart_items.clear()
        self.calculate_totals()

        print("DEBUG: Refreshing product list...")
        self.fetch_and_store_products()
        self.display_products()


    def setup_clock(self):

        current = QDateTime.currentDateTime()
        if hasattr(self.page, 'date'):
            self.page.date.setDate(current.date())
        if hasattr(self.page, 'time'):
            self.page.time.setDisplayFormat("hh:mm:ss AP")
            self.page.time.setTime(current.time())

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def update_clock(self):

        if hasattr(self.page, 'time'):
            self.page.time.setTime(QDateTime.currentDateTime().time())

    def setup_logout(self):

        if hasattr(self.page, 'Logout'):
            self.page.Logout.clicked.connect(self.confirm_logout)

    def confirm_logout(self):
        msg = QMessageBox(self.page)
        msg.setWindowTitle("Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            if hasattr(self, 'timer'):
                self.timer.stop()
            self.page.close()
            self.application.logout()

