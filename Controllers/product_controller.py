from PyQt6.QtWidgets import QTableWidget, QPushButton, QHeaderView, QWidget, QHBoxLayout, QTableWidgetItem, QMessageBox
from functools import partial
from View.dialog.Addproduct import AddProduct
import random


class ProductController:
    def __init__(self, productlist_pages, adminWindow_controller):
        self.productlist_pages = productlist_pages
        self.adminWindow_controller = adminWindow_controller
        self.db = self.adminWindow_controller.db
