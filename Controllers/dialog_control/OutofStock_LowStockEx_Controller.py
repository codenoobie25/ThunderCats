from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QColor


class OutofStockLowStockExCntroller:
    def __init__(self, view, data):
        self.view = view
        self.data = data

        self.load_data_into_table()

    def load_data_into_table(self):
        # --- CHECK YOUR OBJECT NAME ---
        # Replace 'tableWidget' with the actual objectName of your table in Qt Designer
        if not hasattr(self.view, 'tableWidget'):
            print("⚠️ Error: Could not find 'tableWidget' in OutStockDialog.")
            return

        table = self.view.tableWidget

        # Clear existing rows
        table.setRowCount(0)

        for row_index, row_data in enumerate(self.data):
            # Extract data from tuple
            product_name = row_data[0]  # Column 0 from DB
            stock_qty = row_data[1]  # Column 1 from DB

            # Determine Status
            if stock_qty == 0:
                status_text = "Out of Stock"
                status_color = QColor("#FF0000")  # Red
            else:
                status_text = "Low Stock"
                status_color = QColor("#FFD500")  # Yellow/Orange

            # Insert a new row
            table.insertRow(row_index)

            # 1. Product Name Column
            table.setItem(row_index, 0, QTableWidgetItem(str(product_name)))

            # 2. Current Stock Column
            stock_item = QTableWidgetItem(str(stock_qty))
            table.setItem(row_index, 1, stock_item)

            # 3. Status Column
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(status_color)  # Set text color
            table.setItem(row_index, 2, status_item)