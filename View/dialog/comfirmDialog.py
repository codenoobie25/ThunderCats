import os
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, Qt


class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        ui_path = os.path.join(project_root, 'UI', 'Confirm_Dialogs.ui')

        try:
            loadUi(ui_path, self)
        except FileNotFoundError:
            print(f"❌ Error: {ui_path} not found")
            return

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if hasattr(self, 'confirmButton'):
            self.confirmButton.clicked.connect(self.accept)
        elif hasattr(self, 'YesBtn'):
            self.YesBtn.clicked.connect(self.accept)

        if hasattr(self, 'cancelButton'):
            self.cancelButton.clicked.connect(self.reject)
        elif hasattr(self, 'NoBtn'):
            self.NoBtn.clicked.connect(self.reject)