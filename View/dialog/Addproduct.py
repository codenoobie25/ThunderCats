from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class AddProduct(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UI/Add_product.ui", self)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        # import os
        # from PyQt6.QtWidgets import QDialog
        # from PyQt6.uic import loadUi
        # from PyQt6.QtCore import Qt

        # class ProductFormDialog(QDialog):
        #     def __init__(self, parent=None):
        #         super().__init__(parent)
        #
        #         # --- PATH FIX ---
        #         current_dir = os.path.dirname(os.path.abspath(__file__))
        #         project_root = os.path.dirname(os.path.dirname(current_dir))
        #         ui_path = os.path.join(project_root, 'UI', 'Add_product.ui')
        #
        #         try:
        #             loadUi(ui_path, self)
        #         except FileNotFoundError:
        #             print(f"❌ Error: {ui_path} not found")
        #             return
        #
        #