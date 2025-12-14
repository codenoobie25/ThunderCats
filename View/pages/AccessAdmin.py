from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from View.dialog.AddRole import AddRoles

class AccessAdmin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("UI/Accessadmin_page.ui", self)
        print("Access page is loaded ")

        self.addRoles = AddRoles()

        self.Addrole.clicked.connect(self.openAddRoles)

    def openAddRoles(self):
        addRoles = AddRoles()
        addRoles.exec()
