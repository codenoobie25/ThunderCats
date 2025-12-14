import sys
from PyQt6.QtWidgets import QApplication

from Model.database import Database
from View.mainwindow.loginWindow import Loginwindow
from View.mainwindow.AdminWindow import AdminWindow
from Controllers.login_controller import LoginController
from Controllers.admin_controller import Adminwindow


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = Database()

        self.login_window = None
        self.admin_window = None
        self.login_controller = None
        self.admin_controller = None

        self.show_login()

    def show_login(self):
        self.login_window = Loginwindow()
        # Connect Login Controller
        self.login_controller = LoginController(self.login_window, self.db, self)
        self.login_window.show()

    def show_mainwindow(self, role,lastname,firstname):
        print(f"🚀 Switching to {role} Dashboard")

        if role == "Admin":
            self.admin_window = AdminWindow()
            self.admin_controller = Adminwindow(self.admin_window,self.db,self, lastname,firstname)
            self.admin_window.show()

        elif role == "Cashier":
            print("Cashier window coming soon...")

    def logout(self):
        print("🔄 return to Login...")
        self.show_login()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = MainApp()
    app.run()