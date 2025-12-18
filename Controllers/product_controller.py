from Model.products_db import ProductsDatabase
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QDialog, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from View.dialog.Addproduct import AddProduct

class ProductController:
    def __init__(self, productlist_pages, adminWindow_controller):
        self.productlist_pages = productlist_pages
        self.adminWindow_controller = adminWindow_controller
        self.db = ProductsDatabase(self.adminWindow_controller.db)
        self.setup_ui()
        self.load_products()
        self.load_categories()

    def setup_ui(self):
        self.productlist_pages.addProduct.clicked.connect(self.show_add_product_dialog)

        if hasattr(self.productlist_pages, 'refresh_btn'):
            self.productlist_pages.refresh_btn.clicked.connect(self.load_products)

        self.productlist_pages.product_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.productlist_pages.product_table.customContextMenuRequested.connect(self.show_context_menu)

    def load_products(self):
        products = self.db.get_all_products()
        table = self.productlist_pages.product_table

        table.setRowCount(0)

        # Set column count
        table.setColumnCount(8)

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

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Edit Product")
        edit_btn.clicked.connect(lambda: self.edit_product(product_id))
        edit_btn.setFixedSize(30, 25)

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
                if cat_id == product[6]:  # categoryID
                    dialog.combocategories.setCurrentIndex(i)

        if hasattr(dialog, 'prices'):
            dialog.prices.setValue(float(product[3])) # price

        if hasattr(dialog, 'Stockqty'):
            dialog.Stockqty.setValue(int(product[5])) # stock

        if hasattr(dialog, 'warraty'):
            dialog.warraty.setText(str(product[7]))  # warranty

        # Connect save button
        if hasattr(dialog, 'addproductButton'):
            dialog.addproductButton.clicked.connect(lambda: self.update_product(product_id, dialog))
        if hasattr(dialog, 'cancelButton'):
            dialog.cancelButton.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()

    def edit_product(self, product_id):
        print(f"DEBUG: Editing product {product_id}")
        try:
            self.show_edit_product_dialog(product_id)
        except Exception as e:
            print(f"ERROR in edit_product: {e}")
            import traceback
            traceback.print_exc()

    def save_product(self, dialog):
        try:
            name = dialog.addproductName.text().strip() if hasattr(dialog, 'addproductName') else ""
            category_id = dialog.combocategories.currentData() if hasattr(dialog, 'combocategories') else None

            price = dialog.prices.value() if hasattr(dialog, 'prices') else 0.0
            stock = dialog.Stockqty.value() if hasattr(dialog, 'Stockqty') else 0

            warranty = dialog.warraty.text() if hasattr(dialog, 'warraty') else ""
            # Validate
            if not name or not category_id:
                QMessageBox.warning(self.productlist_pages, "Error", "Please fill all required fields!")
                return
            if stock == 0:
                status = "Out of Stock"
            elif stock <= 5:
                status = "Low Stock"
            else:
                status = "In Stock"

            sku = self.db.generate_sku()
            product_id = self.db.generate_product_id()
            success = self.db.add_product(product_id,name, sku, category_id, price, stock, warranty,status)

            if success:
                QMessageBox.information(self.productlist_pages, "Success", "Product added successfully!")
                dialog.accept()
            else:
                QMessageBox.critical(self.productlist_pages, "Error", "Failed to add product!")

        except ValueError as e:
            QMessageBox.warning(self.productlist_pages, "Error", f"Invalid number format: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self.productlist_pages, "Error", f"An error occurred: {str(e)}")
            print(f"ERROR in save_product: {e}")
            import traceback
            traceback.print_exc()

    def update_product(self, product_id, dialog):
        """Update existing product in database"""
        try:
            name = dialog.addproductName.text() if hasattr(dialog, 'addproductName') else ""
            category_id = dialog.combocategories.currentData() if hasattr(dialog, 'combocategories') else None

            price_text = dialog.prices.text() if hasattr(dialog, 'prices') else ""
            price = float(price_text) if price_text else 0.0

            stock_text = dialog.Stockqty.text() if hasattr(dialog, 'Stockqty') else ""
            stock = int(stock_text) if stock_text else 0

            warranty = dialog.warraty.text() if hasattr(dialog, 'warraty') else ""

            # Validate
            if not name or not category_id:
                QMessageBox.warning(self.productlist_pages, "Error", "Please fill all required fields!")
                return

            if stock == 0:
                status = "Out of Stock"
            elif stock <= 5:
                status = "Low Stock"
            else:
                status = "In Stock"

            # Update in database
            success = self.db.update_product(product_id, name, category_id, price, stock, warranty, status)

            if success:
                QMessageBox.information(self.productlist_pages, "Success", "Product updated successfully!")
                dialog.accept()
            else:
                QMessageBox.critical(self.productlist_pages, "Error", "Failed to update product!")

        except ValueError as e:
            QMessageBox.warning(self.productlist_pages, "Error", f"Invalid number format: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self.productlist_pages, "Error", f"An error occurred: {str(e)}")
            print(f"ERROR in update_product: {e}")
            import traceback
            traceback.print_exc()

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
        pass