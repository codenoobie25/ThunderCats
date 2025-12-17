
class CashierController:
    def __init__(self, cashierwindow, db, application):
        self.page = cashierwindow
        self.db = db
        self.application = application