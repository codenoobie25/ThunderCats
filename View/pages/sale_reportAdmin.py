import sys
import csv
import datetime
import platform
import subprocess
import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem,
    QLabel, QPushButton, QFileDialog, QApplication
)
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

# --- Library for Chart generation ---
import matplotlib

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# --- Library for PDF generation ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- MOCK DATA (Sample Data for Charts/Cards) ---
MOCK_SALES_DATA = [
    {"item_name": "RTX 4090", "category": "GPU", "price": 1599.99, "sale_date": datetime.date.today()},
    {"item_name": "Intel i9-13900K", "category": "CPU", "price": 589.99, "sale_date": datetime.date.today()},
    {"item_name": "Samsung 990 Pro", "category": "Storage", "price": 169.99, "sale_date": datetime.date.today()},
    {"item_name": "Corsair 32GB RAM", "category": "Memory", "price": 129.99,
     "sale_date": datetime.date.today() - datetime.timedelta(days=1)},
    {"item_name": "RTX 4070", "category": "GPU", "price": 599.99,
     "sale_date": datetime.date.today() - datetime.timedelta(days=2)},
    {"item_name": "Asus ROG Motherboard", "category": "Motherboard", "price": 299.99,
     "sale_date": datetime.date.today() - datetime.timedelta(days=5)},
    {"item_name": "Lian Li Case", "category": "Case", "price": 149.99,
     "sale_date": datetime.date.today() - datetime.timedelta(days=10)},
]


class ReportItemWidget(QWidget):
    """
    CUSTOM WIDGET: This puts the 'Open File' button inside the list row.
    """

    def __init__(self, report_name, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

        # Layout for the row
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Icon/Text
        self.lbl_name = QLabel(f"📄 {report_name}")
        # Assuming you use a dark theme, we adjust colors for visibility
        self.lbl_name.setStyleSheet("font-weight: bold;")

        # The Open Button
        self.btn_open = QPushButton("Open File")
        self.btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0; border: none; border-radius: 4px;
                padding: 5px 10px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background-color: #cbd5e1; }
        """)
        self.btn_open.clicked.connect(self.open_file)

        layout.addWidget(self.lbl_name)
        layout.addStretch()
        layout.addWidget(self.btn_open)

    def open_file(self):
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', self.file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(self.file_path)
            else:  # Linux
                subprocess.call(('xdg-open', self.file_path))
        except Exception as e:
            print(f"Could not open file: {e}")


class SaleReportAdmin(QWidget):
    def __init__(self):
        super().__init__()

        # 1. Load the UI from your specific folder
        try:
            loadUi("UI/sale_reportAdmin_page.ui", self)
            print("Sale report page is loaded successfully.")
        except FileNotFoundError:
            print("ERROR: Could not find 'UI/sale_reportAdmin_page.ui'. Check your folder structure.")
            return

        # 2. Setup all the logic (Cards, Charts, Buttons)
        self.setup_ui_logic()

    def setup_ui_logic(self):
        """Initializes all the functional parts of the page."""

        # A. Populate Filter Combo
        if hasattr(self, 'combo_period'):
            self.combo_period.clear()
            self.combo_period.addItems(["This Day", "This Weekend", "This Month", "Full Report"])

        # B. Connect Export Button
        if hasattr(self, 'btn_export'):
            self.btn_export.clicked.connect(self.handle_export)

        # C. Calculate Data & Draw Charts
        self.update_summary_cards()
        self.init_chart()
        self.add_sample_reports()

    def update_summary_cards(self):
        """Calculates totals and updates the 3 purple cards."""
        try:
            total_sales = sum(item['price'] for item in MOCK_SALES_DATA)
            count = len(MOCK_SALES_DATA)
            avg_ticket = total_sales / count if count > 0 else 0

            # Find Top Category
            cat_counts = {}
            for item in MOCK_SALES_DATA:
                c = item['category']
                cat_counts[c] = cat_counts.get(c, 0) + item['price']
            top_cat = max(cat_counts, key=cat_counts.get) if cat_counts else "N/A"

            # Update Labels (Ensure objectNames match in Qt Designer!)
            self.lbl_revenue.setText(f"${total_sales:,.2f}")
            self.lbl_ticket.setText(f"${avg_ticket:,.2f}")
            self.lbl_category.setText(str(top_cat))

        except AttributeError as e:
            print(f"UI Error (Cards): Missing a label objectName. Details: {e}")

    def init_chart(self):
        """Draws the Matplotlib chart inside 'widget_chart_container'."""
        if hasattr(self, 'widget_chart_container'):
            # Clear previous chart if any
            if self.widget_chart_container.layout() is None:
                layout = QVBoxLayout(self.widget_chart_container)
                layout.setContentsMargins(0, 0, 0, 0)
            else:
                layout = self.widget_chart_container.layout()
                # Clear old widgets
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget(): child.widget().deleteLater()

            # Create Chart
            fig = Figure(figsize=(5, 4), dpi=100)
            fig.patch.set_alpha(0)  # Transparent background
            canvas = FigureCanvasQTAgg(fig)
            layout.addWidget(canvas)

            # Data Processing
            cat_totals = {}
            for item in MOCK_SALES_DATA:
                c = item['category']
                cat_totals[c] = cat_totals.get(c, 0) + item['price']

            cats = list(cat_totals.keys())
            revs = list(cat_totals.values())
            colors = ['#22c55e', '#3b82f6', '#a855f7', '#f97316', '#94a3b8']

            # Plot
            ax = fig.add_subplot(111)
            ax.set_facecolor('none')

            # Handle color cycling
            bar_colors = colors[:len(cats)] if len(cats) <= len(colors) else colors * (len(cats) // len(colors) + 1)

            bars = ax.barh(cats, revs, color=bar_colors)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_color('#ffffff')  # White axis line for dark theme
            ax.tick_params(axis='x', colors='white')  # White text
            ax.tick_params(axis='y', colors='white')  # White text
            ax.invert_yaxis()
            fig.tight_layout()
        else:
            print("UI Error: 'widget_chart_container' not found.")

    def handle_export(self):
        """Handles the Save As Dialog and File Generation."""
        period = self.combo_period.currentText()
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        default_name = f"ThunderCats_Report_{date_str}_{period.replace(' ', '')}"

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Sales Report",
            default_name,
            "CSV Files (*.csv);;PDF Files (*.pdf)"
        )

        if not file_path:
            return

            # In a real app, you would filter data based on 'period' here
        data = MOCK_SALES_DATA

        if selected_filter == "CSV Files (*.csv)":
            if not file_path.endswith('.csv'): file_path += '.csv'
            self.generate_csv(file_path, data, period)
        else:
            if not file_path.endswith('.pdf'): file_path += '.pdf'
            self.generate_pdf(file_path, data, period)

        self.add_report_to_list(file_path)

    def generate_csv(self, filepath, data, title):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([f"ThunderCats Report: {title}"])
                writer.writerow(["Item", "Category", "Price", "Date"])
                for row in data:
                    writer.writerow([row['item_name'], row['category'], row['price'], row['sale_date']])
            print(f"CSV Generated: {filepath}")
        except Exception as e:
            print(f"Error writing CSV: {e}")

    def generate_pdf(self, filepath, data, title):
        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            y = 750
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, f"ThunderCats Sales Report: {title}")
            y -= 30
            c.setFont("Helvetica", 12)

            for row in data:
                if y < 50:
                    c.showPage()
                    y = 750
                line = f"{row['item_name']}  |  {row['category']}  |  ${row['price']}"
                c.drawString(50, y, line)
                y -= 20
            c.save()
            print(f"PDF Generated: {filepath}")
        except Exception as e:
            print(f"Error writing PDF: {e}")

    def add_sample_reports(self):
        """Adds some fake initial reports."""
        self.add_report_to_list("/tmp/Sample_Report_2023.pdf")

    def add_report_to_list(self, file_path):
        file_name = os.path.basename(file_path)

        # Create Custom Widget
        custom_widget = ReportItemWidget(file_name, file_path)

        # Add to List
        if hasattr(self, 'listWidget_reports'):
            item = QListWidgetItem(self.listWidget_reports)
            item.setSizeHint(custom_widget.sizeHint())
            self.listWidget_reports.addItem(item)
            self.listWidget_reports.setItemWidget(item, custom_widget)
        else:
            print("UI Error: 'listWidget_reports' not found.")


# --- Only for testing standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaleReportAdmin()
    window.show()
    sys.exit(app.exec())