from PyQt6.QtWidgets import QTableWidget, QPushButton, QHeaderView, QWidget, QHBoxLayout, QTableWidgetItem, QMessageBox
from functools import partial
from View.dialog.Addproduct import AddProduct
import random


class ProductController:
    def __init__(self, admin_window, db):
        self.main_view = admin_window
        self.db = db

        print("🔍 Controller: Hunting for widgets inside the Stack...")

        # --- THE FIX: USE findChild() ---
        # This searches EVERY page of your stack widget to find the ID.

        # 1. Hunt for the Table (Try specific names)
        self.table = self.main_view.findChild(QTableWidget, "tableWidget")

        # 2. Hunt for the Add Button
        self.add_btn = self.main_view.findChild(QPushButton, "btnAddProduct")

        # --- DEBUG CHECK ---
        if self.table is None:
            print("❌ CRITICAL: Could not find 'tableWidget' anywhere in the stack!")
            # Lets try to find ANY table to help you debug
            all_tables = self.main_view.findChildren(QTableWidget)
            if all_tables:
                print(f"   -> Found these tables instead: {[t.objectName() for t in all_tables]}")
            return  # STOP HERE to prevent crash
        else:
            print(f"✅ Found Table: {self.table.objectName()}")

        if self.add_btn is None:
            print("⚠️ WARNING: Could not find 'btnAddProduct'. Add button will not work.")
            all_btns = self.main_view.findChildren(QPushButton)
            print(f"   -> Found buttons: {[b.objectName() for b in all_btns]}")
        else:
            print(f"✅ Found Button: {self.add_btn.objectName()}")
            self.add_btn.clicked.connect(self.open_add_dialog)

        # --- SETUP TABLE ---
        # Now we use 'self.table' instead of 'self.view.tableWidget'
        self.setup_table_structure()
        self.load_product_table()

    def setup_table_structure(self):
        """ Force the column structure to match your code """
        self.table.setColumnCount(9)
        headers = ["ID", "Name", "SKU", "Category", "Price", "Stock", "Status", "Warranty", "Action"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_product_table(self):
        print("📥 Loading data...")
        products = self.db.get_all_products()

        self.table.setRowCount(0)

        for row, p in enumerate(products):
            self.table.insertRow(row)

            # Safe Data Extraction
            p_id = str(p['product_id'])
            name = str(p['name']) if p['name'] else "Unknown"
            sku = str(p['sku']) if p['sku'] else "New"
            cat = str(p['categoryName']) if p['categoryName'] else "-"
            price = f"₱ {float(p['price']):,.2f}" if p['price'] else "₱ 0.00"
            stock = str(p['stock_quantity'])
            status = str(p['Status']) if p['Status'] else "Active"
            warranty = str(p['warranty']) if p['warranty'] else "-"

            # Fill Cells
            self.table.setItem(row, 0, QTableWidgetItem(p_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(sku))
            self.table.setItem(row, 3, QTableWidgetItem(cat))
            self.table.setItem(row, 4, QTableWidgetItem(price))
            self.table.setItem(row, 5, QTableWidgetItem(stock))
            self.table.setItem(row, 6, QTableWidgetItem(status))
            self.table.setItem(row, 7, QTableWidgetItem(warranty))

            # Add Buttons
            self.add_action_buttons(row, p['product_id'])

    def add_action_buttons(self, row, product_id):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(5)

        btn_edit = QPushButton("Edit")
        btn_edit.setStyleSheet("background-color: #FFD500; color: #2A004E; font-weight: bold;")
        btn_edit.clicked.connect(partial(self.handle_edit, product_id))

        btn_del = QPushButton("Del")
        btn_del.setStyleSheet("background-color: #FF4444; color: white; font-weight: bold;")
        btn_del.clicked.connect(partial(self.handle_delete, product_id))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_del)

        self.table.setCellWidget(row, 8, widget)

    def handle_delete(self, pid):
        if self.db.delete_product(pid):
            self.load_product_table()

    def handle_edit(self, pid):
        # Your existing edit logic here...
        pass

    def open_add_dialog(self):
        # Your existing add logic here...
        # Reuse the working dialog code from previous steps
        pass