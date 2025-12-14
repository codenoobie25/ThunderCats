from PyQt6.QtWidgets import QMessageBox


class LoginController:
    def __init__(self, login_view, db, main_app):
        self.view = login_view
        self.db = db
        self.main_app = main_app


        self.username = None
        self.password = None
        self.role = None
        self.view.LoginBtn.clicked.connect(self.attempt_login)

    def attempt_login(self):
        self.username = self.view.lineEdit_Username.text()
        self.password = self.view.lineEdit_Password.text()

        print(f"Controller: Checking {self.username}...")

        # 2. Check DB
        if self.db.validate_login(self.username, self.password): self.login_success()
        else:
            self.login_fail()

    def login_success(self):
        print("✅ Login Success!")
        self.role = self.db.get_user_role()

        self.view.close()

        self.main_app.show_mainwindow(self.role)

    def login_fail(self):
        print("❌ Login Failed.")
        QMessageBox.warning(self.view, "Login Error", "Invalid Username or Password")