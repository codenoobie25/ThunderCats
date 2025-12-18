from PyQt6.QtWidgets import QMessageBox
from Controllers.dialog_control.receipt_controller import ReceiptC_C_C


class CheckoutCashierController:
    def __init__(self, checkout_ui, sales_db,cart_items=None, cashier_controller=None):
        self.ui = checkout_ui
        self.sales_db = sales_db
        self.cart_items = cart_items if cart_items else []
        self.cashier_controller = cashier_controller

        self.ui.completeOrder.clicked.connect(self.complete_order)
        self.ui.changedue2.textChanged.connect(self.calculate_change)

        if hasattr(self.ui, 'cancelButton'):
            self.ui.cancelButton.clicked.connect(self.cancel_checkout)

        self.update_display()

    def cancel_checkout(self):
        self.ui.close()

    def update_display(self):
        subtotal = sum(item['subtotal'] for item in self.cart_items)
        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax, 2)

        self.ui.subtotal.setText(f"{subtotal:.2f}")
        self.ui.taxs.setText(f"{tax:.2f}")
        self.ui.Totalamountdue.setText(f"{total:.2f}")

        self.calculate_change()

    def calculate_change(self):
        try:
            cash_text = self.ui.changedue2.text()
            if cash_text:
                cash_tendered = float(cash_text)
                total = self.get_total()
                change = round(cash_tendered - total, 2)
                self.ui.changedues.setText(f"{change:.2f}")
            else:
                self.ui.changedues.setText("0.00")
        except ValueError:
            self.ui.changedues.setText("0.00")

    def get_total(self):
        subtotal = sum(item['subtotal'] for item in self.cart_items)
        tax = round(subtotal * 0.08, 2)
        return round(subtotal + tax, 2)

    def complete_order(self):
        try:
            print("=" * 50)

            if not self.cart_items:
                QMessageBox.warning(self.ui, "Empty Cart", "Please add items to cart first.")
                return

            try:
                cash_tendered = float(self.ui.changedue2.text())
                print(f"DEBUG: Cash tendered: {cash_tendered}")
            except ValueError:
                QMessageBox.warning(self.ui, "Invalid Input", "Please enter cash amount.")
                return

            total = self.get_total()

            if cash_tendered < total:
                QMessageBox.warning(self.ui, "Insufficient Payment",
                                    f"Cash tendered (₱{cash_tendered:.2f}) is less than total (₱{total:.2f}).")
                return

            confirm = QMessageBox.question(self.ui, "Confirm Order",
                                           f"Complete order for ₱{total:.2f}?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if confirm == QMessageBox.StandardButton.Yes:
                print("DEBUG: User confirmed order")
                print(f"DEBUG: sales_db object: {self.sales_db}")
                print(f"DEBUG: sales_db type: {type(self.sales_db)}")

                # Process transaction
                result = self.sales_db.complete_transaction(
                    self.cart_items,
                    "Cash",
                    cash_tendered
                )


                if result:
                    print("DEBUG: Transaction successful")

                    # Clear parent's cart
                    if self.cashier_controller:
                        self.cashier_controller.clear_cart_after_checkout()

                    # Close checkout dialog
                    self.ui.close()

                    # Show receipt
                    self.show_receipt(result)

                    QMessageBox.information(None, "Success",
                                            f"Transaction completed!\nReceipt: {result['receipt_number']}")
                else:
                    QMessageBox.critical(self.ui, "Error", "Failed to process transaction.")


        except Exception as e:
            print(f"ERROR in complete_order: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.ui, "Error", f"An error occurred: {str(e)}")

    def show_receipt(self, transaction_data):
        try:
            self.receipt_controller = ReceiptC_C_C(transaction_data)
            self.receipt_controller.show()
        except Exception as e:
            print(f"ERROR in show_receipt: {e}")
            import traceback
            traceback.print_exc()