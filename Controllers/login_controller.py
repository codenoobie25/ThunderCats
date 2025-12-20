from PyQt6.QtWidgets import QMessageBox, QLineEdit


class LoginController:
    def __init__(self, login_view, db, main_app):
        self.view = login_view
        self.db = db
        self.main_app = main_app

        self.username = None
        self.password = None
        self.role = None
        self.view.showpassword.stateChanged.connect(self.toggle_password_visibility)
        self.view.LoginBtn.clicked.connect(self.attempt_login)

    def attempt_login(self):
        self.username = self.view.lineEdit_Username.text()
        self.password = self.view.lineEdit_Password.text()

        print(f"Controller: Checking {self.username}...")

        try:
            is_valid = self.db.validate_login(self.username, self.password)
            print(f"DEBUG: Database validation result: {is_valid}")

            if is_valid:
                self.role = self.db.get_user_type(self.username)
                self.login_success()
            else:
                self.login_fail()
        except Exception as e:
            print(f"DEBUG: Login error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view, "Login Error", f"System Error: {str(e)}")

    def login_success(self):
        print("✅ Login Success!")
        role_tuple =self.db.get_user_type(self.username)
        self.role = role_tuple[0]

        self.view.close()
        self.main_app.show_mainwindow(self.role)

    def login_fail(self):
        print("❌ Login Failed.")
        QMessageBox.warning(self.view, "Login Error", "Invalid Username or Password")

    def toggle_password_visibility(self):
        if self.view.showpassword.isChecked():
            self.view.lineEdit_Password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.view.lineEdit_Password.setEchoMode(QLineEdit.EchoMode.Password)