from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class ProductCardWidget(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, p_id, name, price, parent=None):
        super().__init__(parent)
        self.product_id = p_id

        self.setFixedSize(180, 180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("ProductCard")

        self.setStyleSheet("""
            QFrame#ProductCard {
                background-color: #2A004E;
                border: 2px solid #4a148c;
                border-radius: 15px;
            }
            QFrame#ProductCard:hover {
                border: 2px solid #ffd500;
                background-color: #350060;
            }
            QLabel {
                border: none;
                background-color: transparent;
                color: white;
            }
            QLabel#icon {
                font-size: 30px;
                color: #b39ddb;
            }
            QLabel#name {
                font-size: 13px;
                font-weight: bold;
                padding: 5px;
            }
            QLabel#price {
                color: #ffd500;
                font-size: 15px;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        self.lbl_icon = QLabel("⚡")
        self.lbl_icon.setObjectName("icon")
        self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_name = QLabel(name)
        self.lbl_name.setObjectName("name")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_price = QLabel(f"₱ {price:,.2f}")
        self.lbl_price.setObjectName("price")
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.lbl_icon)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_price)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.product_id)
        super().mousePressEvent(event)


class CartItemWidget(QWidget):
    qty_changed = pyqtSignal()
    item_removed = pyqtSignal(int)

    def __init__(self, p_id, name, price, parent=None):
        super().__init__(parent)
        self.product_id = p_id
        self.unit_price = price
        self.quantity = 1

        self.setFixedHeight(80)
        self.setStyleSheet("""
            QWidget#cartItem {
                background-color: #320b5e;
                border-radius: 10px;
                border: 1px solid #4a148c;
            }
            QLabel { color: white; border: none; background: transparent; }
            QPushButton {
                background-color: #1a0530; color: white;
                border: 1px solid #5e35b1; border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ffd500; color: black; }
            QPushButton#btnDelete {
                background-color: transparent; border: none; font-size: 18px; color: #ef5350;
            }
            QPushButton#btnDelete:hover { color: red; }
        """)
        self.setObjectName("cartItem")

        layout = QHBoxLayout()

        info_layout = QVBoxLayout()
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.lbl_price = QLabel(f"₱ {price:,.2f}")
        self.lbl_price.setStyleSheet("color: #ffd500;")
        info_layout.addWidget(self.lbl_name)
        info_layout.addWidget(self.lbl_price)

        btn_minus = QPushButton("−")
        btn_minus.setFixedSize(30, 30)
        self.lbl_qty = QLabel("1")
        self.lbl_qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_qty.setFixedWidth(20)
        btn_plus = QPushButton("+")
        btn_plus.setFixedSize(30, 30)
        btn_delete = QPushButton("🗑")
        btn_delete.setObjectName("btnDelete")
        btn_delete.setFixedSize(30, 30)

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(btn_minus)
        layout.addWidget(self.lbl_qty)
        layout.addWidget(btn_plus)
        layout.addSpacing(5)
        layout.addWidget(btn_delete)
        self.setLayout(layout)

        btn_plus.clicked.connect(self.increase_qty)
        btn_minus.clicked.connect(self.decrease_qty)
        btn_delete.clicked.connect(self.remove_self)

    def increase_qty(self):
        self.quantity += 1
        self.lbl_qty.setText(str(self.quantity))
        self.qty_changed.emit()

    def decrease_qty(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.lbl_qty.setText(str(self.quantity))
            self.qty_changed.emit()

    def remove_self(self):
        self.item_removed.emit(self.product_id)

    def get_subtotal(self):
        return self.quantity * self.unit_price