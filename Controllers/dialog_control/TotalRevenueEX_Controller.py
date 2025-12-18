from PyQt6.QtWidgets import QLabel


class TotalRevenueEXController:
    def __init__(self, view, data):

        self.view = view
        self.data = data

        self.update_ui()

    def update_ui(self):

        if hasattr(self.view, 'grosssale'):
            formatted_sale = "{:,.2f}".format(self.data['gross_sale'])
            self.view.grosssale.setText(formatted_sale)

        if hasattr(self.view, 'totaltransac'):
            self.view.totaltransac.setText(str(self.data['total_transactions']))

        if hasattr(self.view, 'totalsold'):
            self.view.totalsold.setText(str(self.data['total_items_sold']))

        payment_counts = self.data['payment_counts']

        if hasattr(self.view, 'totalcash'):
            count = payment_counts.get('Cash', 0)
            self.view.totalcash.setText(str(count))

        if hasattr(self.view, 'totalcard'):
            count = payment_counts.get('Credit Card', 0)
            self.view.totalcard.setText(str(count))

        if hasattr(self.view, 'totalEwallet'):
            count = payment_counts.get('E-wallet', 0)
            self.view.totalEwallet.setText(str(count))