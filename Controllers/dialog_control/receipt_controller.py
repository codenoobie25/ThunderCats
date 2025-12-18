from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel

from View.dialog.checkout_cashierUI import Receipt
from datetime import datetime

    #ReceiptCheckOutCashierController
class ReceiptC_C_C:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data

        self.dialog = Receipt()
        self.ui = self.dialog

    def populate_receipt(self):
        data = self.transaction_data

        self.ui.Receiptnumber.setText(f"Receipt #: {data['receipt_number']}")

        self.ui.subtotal.setText(f"{data['subtotal']:.2f}")
        self.ui.taxs.setText(f"{data['tax_amount']:.2f}")
        self.ui.total.setText(f"{data['total_amount']:.2f}")
        self.ui.totalChange.setText(f"{data['change_amount']:.2f}")

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.datentime.setText(current_date)

        self.ui.transactionID.setText("Transaction ID: " + str(data['sale_id']))

        self.populate_items_scroll_area(data['items'])

    def populate_items_scroll_area(self, items):
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(15, 15, 15, 15)

        receipt_text = "ITEMS PURCHASED\n"
        receipt_text += "═" * 35 + "\n\n"

        for item in items:

            name_qty = f"{item['product_name']} x{item['quantity']}"
            price = f"₱{item['subtotal']:.2f}"


            total_width = 35
            dots_needed = total_width - len(name_qty) - len(price)
            dots = "." * max(dots_needed, 2)

            receipt_text += f"{name_qty}{dots}{price}\n"

        items_label = QLabel(receipt_text)
        items_label.setStyleSheet("""
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.5;
        """)
        items_label.setWordWrap(True)

        scroll_layout.addWidget(items_label)
        scroll_layout.addStretch()

        scroll_widget.setStyleSheet("background-color: #2D1B69;")
        self.ui.receiptsummary.setWidget(scroll_widget)

    def show(self):
        self.populate_receipt()
        self.dialog.exec()