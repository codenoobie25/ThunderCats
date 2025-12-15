from Model.products_db import ProductsDatabase
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QDialog, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class ProductController:
    def __init__(self, productlist_pages, adminWindow_controller):
        self.productlist_pages = productlist_pages
        self.adminWindow_controller = adminWindow_controller
        self.db = ProductsDatabase(self.adminWindow_controller.db)
        self.setup_ui()
        self.load_products()
        self.load_categories()

    def setup_ui(self):
        """Connect UI signals to controller methods"""
        # Connect add button
        self.productlist_pages.addProduct.clicked.connect(self.show_add_product_dialog)

        # Connect refresh button if exists
        if hasattr(self.productlist_pages, 'refresh_btn'):
            self.productlist_pages.refresh_btn.clicked.connect(self.load_products)

        # Setup table context menu
        self.productlist_pages.product_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.productlist_pages.product_table.customContextMenuRequested.connect(self.show_context_menu)

    def load_products(self):
        """Load all products into the table"""
        products = self.db.get_all_products()
        table = self.productlist_pages.product_table

        # Clear existing rows
        table.setRowCount(0)

        # Set column count
        table.setColumnCount(8)  # product_id, name, sku, category, price, stock, status, warranty

        # Set headers
        headers = ["ID", "Name", "SKU", "Category", "Price", "Stock", "Status", "Warranty", "Actions"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Populate data
        for row, product in enumerate(products):
            table.insertRow(row)

            # Add data to cells
            for col, data in enumerate(product):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable
                table.setItem(row, col, item)

            self.add_action_buttons(row, product[0])

    def add_action_buttons(self, row, product_id):

        table = self.productlist_pages.product_table

        # Create widget for buttons
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        # Edit button
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Edit Product")
        edit_btn.clicked.connect(lambda: self.edit_product(product_id))
        edit_btn.setFixedSize(30, 25)

        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete Product")
        delete_btn.clicked.connect(lambda: self.delete_product(product_id))
        delete_btn.setFixedSize(30, 25)

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

        table.setCellWidget(row, table.columnCount() - 1, widget)

    def load_categories(self):

        self.categories = self.db.get_all_categories()

    def show_add_product_dialog(self):
        from View.dialog.Addproduct import AddProduct  # Import here to avoid circular imports

        dialog = AddProduct()
        dialog.setWindowTitle("Add Product")

        # Populate category combobox
        if hasattr(dialog, 'combocategories'):
            dialog.combocategories.clear()
            for category_id, category_name in self.categories:
                dialog.combocategories.addItem(category_name, category_id)

        # Connect dialog buttons
        if hasattr(dialog, 'addproductButton'):
            dialog.addproductButton.clicked.connect(lambda: self.save_product(dialog))
        if hasattr(dialog, 'cancelButton'):
            dialog.cancelButton.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()  # Refresh table

    def show_edit_product_dialog(self, product_id):
        """Show dialog for editing existing product"""
        from View.dialog.Addproduct import AddProduct

        # Get product data
        product = self.db.get_product_by_id(product_id)
        if not product:
            QMessageBox.warning(self.productlist_pages, "Error", "Product not found!")
            return

        dialog = AddProduct()
        dialog.setWindowTitle("Edit Product")
        if hasattr(dialog, 'header'):
            dialog.header.setText("Edit Product")

        if hasattr(dialog, 'addproductName'):
            dialog.addproductName.setText(product[1])  # name

        if hasattr(dialog, 'combocategories'):
            dialog.combocategories.clear()
            for i, (cat_id, cat_name) in enumerate(self.categories):
                dialog.combocategories.addItem(cat_name, cat_id)
                if cat_id == product[3]:  # categoryID
                    dialog.combocategories.setCurrentIndex(i)

        if hasattr(dialog, 'prices'):
            dialog.prices.setText(str(product[4]))  # price

        if hasattr(dialog, 'Stockqty'):
            dialog.Stockqty.setText(str(product[5]))  # stock

        if hasattr(dialog, 'warraty'):
            dialog.warraty.setText(str(product[7]))  # warranty

        # Connect save button
        if hasattr(dialog, 'addproductButton'):
            dialog.addproductButton.clicked.connect(lambda: self.update_product(product_id, dialog))
        if hasattr(dialog, 'cancelButton'):
            dialog.cancelButton.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()  # Refresh table

    def edit_product(self, product_id):
        print(f"DEBUG: Editing product {product_id}")  # Add debug
        try:
            self.show_edit_product_dialog(product_id)
        except Exception as e:
            print(f"ERROR in edit_product: {e}")
            import traceback
            traceback.print_exc()

        
    def save_product(self, dialog):
        print("Dialog attributes:", [attr for attr in dir(dialog) if not attr.startswith('_')])
        name = dialog.addproductName.text() if hasattr(dialog, 'addproductName') else ""
        category_id = dialog.combocategories.currentData() if hasattr(dialog, 'combocategories') else None
        price = float(dialog.prices.text()) if hasattr(dialog, 'prices') and dialog.price_input.text() else 0
        stock = int(dialog.Stockqty.text()) if hasattr(dialog, 'Stockqty') and dialog.stock_input.text() else 0
        warranty = dialog.warraty.text() if hasattr(dialog, 'warraty') else ""

        sku = self.db.generate_sku()
        # Validate
        if not name or not category_id:
            QMessageBox.warning(self.productlist_pages, "Error", "Please fill all required fields!")
            return

        # Save to database
        success = self.db.add_product(name, sku, category_id, price, stock, warranty)

        if success:
            QMessageBox.information(self.productlist_pages, "Success", "Product added successfully!")
            dialog.accept()
        else:
            QMessageBox.critical(self.productlist_pages, "Error", "Failed to add product!")

    def update_product(self, product_id, dialog):
        """Update existing product in database"""
        # Get data from dialog
        name = dialog.addproductName.text() if hasattr(dialog, 'name_input') else ""
        category_id = dialog.combocategories.currentData() if hasattr(dialog, 'category_combo') else None
        price = float(dialog.prices.text()) if hasattr(dialog, 'price_input') and dialog.price_input.text() else 0
        stock = int(dialog.Stockqty.text()) if hasattr(dialog, 'stock_input') and dialog.stock_input.text() else 0
        warranty = dialog.warraty.text() if hasattr(dialog, 'warranty_input') else ""

        # Validate
        if not name or not category_id:
            QMessageBox.warning(self.productlist_pages, "Error", "Please fill all required fields!")
            return

        # Determine status based on stock
        status = "In Stock" if stock > 0 else "Out of Stock"

        # Update in database
        success = self.db.update_product(product_id, name, category_id, price, stock, warranty, status)

        if success:
            QMessageBox.information(self.productlist_pages, "Success", "Product updated successfully!")
            dialog.accept()
        else:
            QMessageBox.critical(self.productlist_pages, "Error", "Failed to update product!")

    def delete_product(self, product_id):
        """Delete product with confirmation"""
        reply = QMessageBox.question(
            self.productlist_pages,
            "Confirm Delete",
            "Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.db.delete_product(product_id)
            if success:
                QMessageBox.information(self.productlist_pages, "Success", "Product deleted successfully!")
                self.load_products()
            else:
                QMessageBox.critical(self.productlist_pages, "Error", "Failed to delete product!")

    def show_context_menu(self, position):
        """Show right-click context menu on table"""
        # You can implement context menu for additional actions
        pass
