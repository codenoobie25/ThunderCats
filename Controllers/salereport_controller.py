import os
from datetime import datetime, timedelta
from PyQt6.QtCore import QDate, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QVBoxLayout, QMessageBox, QTableWidgetItem, QPushButton, QHeaderView
from matplotlib import ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

# --- REPORTLAB IMPORTS (For Text Tables) ---
from reportlab.lib import colors as pdf_colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class SaleReportController:
    def __init__(self, salereport_pages, adminWindow_controller):
        self.ui = salereport_pages
        self.db = adminWindow_controller.db

        self.chart_layout = self.ui.widget_chart_container.layout()
        if self.chart_layout is None:
            self.chart_layout = QVBoxLayout(self.ui.widget_chart_container)

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('#2A004E')
        self.canvas = FigureCanvas(self.figure)
        self.chart_layout.addWidget(self.canvas)

        self.ui.date_start.setCalendarPopup(True)
        self.ui.date_end.setCalendarPopup(True)
        self.ui.date_start.setDate(QDate.currentDate())
        self.ui.date_end.setDate(QDate.currentDate())
        self.ui.date_start.setEnabled(False)
        self.ui.date_end.setEnabled(False)

        self.ui.table_reports.setColumnCount(4)
        self.ui.table_reports.setHorizontalHeaderLabels(["Report Name", "Type", "Date Generated", "Action"])
        header = self.ui.table_reports.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        self.ui.combo_category.currentIndexChanged.connect(self.refresh_report)
        self.ui.combo_period.currentIndexChanged.connect(self.handle_period_change)
        self.ui.btn_export.clicked.connect(self.handle_export)

        try:
            self.refresh_report()
            self.load_reports_history()
        except Exception as e:
            print(f"Error during initial load: {e}")

    def handle_period_change(self):
        period = self.ui.combo_period.currentText()
        is_custom = (period == "Custom Range")
        self.ui.date_start.setEnabled(is_custom)
        self.ui.date_end.setEnabled(is_custom)
        self.refresh_report()

    def get_date_range(self, time_filter):
        clean_filter = time_filter.strip()
        print(f"DEBUG: Selected Filter: '{clean_filter}'")

        if clean_filter == "Custom Range":
            return (self.ui.date_start.date().toString("yyyy-MM-dd 00:00:00"),
                    self.ui.date_end.date().toString("yyyy-MM-dd 23:59:59"))

        now = datetime.now()


        if clean_filter == "This Day":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        elif clean_filter == "This Week":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        elif clean_filter == "This Month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        elif clean_filter == "Full Report":
            start = datetime(2000, 1, 1, 0, 0, 0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        start_str = start.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end.strftime('%Y-%m-%d %H:%M:%S')

        return start_str, end_str

    def refresh_report(self):
        try:
            report_type = self.ui.combo_category.currentText()
            time_period = self.ui.combo_period.currentText()
            start, end = self.get_date_range(time_period)


            stats = self.db.salereportdb.fetch_summary_stats(start, end)
            self.ui.lbl_revenue.setText(f"₱{stats['total_sales']:,.2f}")
            self.ui.lbl_ticket.setText(f"₱{stats['avg_ticket']:,.2f}")
            self.ui.lbl_category.setText(str(stats['top_category']))

            if report_type == "Sale":
                data = self.db.salereportdb.fetch_revenue_by_category(start, end)
                self.ui.header_rev.setText("Revenue by Component")
                self.plot_graph(data, "Revenue")
            elif report_type == "Product":
                data = self.db.salereportdb.fetch_top_products(start, end)
                self.ui.header_rev.setText("Top Selling Products (Qty)")
                self.plot_graph(data, "Quantity")

        except Exception as e:
            print(f"Error in refresh: {e}")

    def plot_graph(self, data, metric_name):
        self.figure.clear()

        if not data:
            self.canvas.draw()
            return

        df = pd.DataFrame(data)

        if metric_name == "Revenue":
            if 'Category' not in df.columns: return
            labels = df['Category'].astype(str).tolist()
            values = df['Revenue'].astype(float).tolist()
            bar_color = '#FFD500'
        else:
            if 'product_name' not in df.columns: return
            labels = df['product_name'].astype(str).tolist()
            values = df['quantity'].astype(int).tolist()
            bar_color = '#00D4FF'


        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#2A004E')
        self.figure.subplots_adjust(bottom=0.3)  # Space for labels

        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        bars = ax.bar(labels, values, color=bar_color, width=0.6)

        ax.tick_params(axis='x', colors='white', labelsize=8, rotation=15)
        ax.tick_params(axis='y', colors='white', labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        for bar in bars:
            height = bar.get_height()
            label_text = f"₱{height:,.2f}" if metric_name == "Revenue" else f"{int(height)}"
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    label_text,
                    ha='center', va='bottom', color='white', fontsize=8)
        self.canvas.draw()

    def handle_export(self):
        confirm = QMessageBox.question(self.ui, "Confirm", "Generate Detailed PDF Report?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No: return

        cat = self.ui.combo_category.currentText()
        period = self.ui.combo_period.currentText()
        date_str = datetime.now().strftime("%Y-%m-%d")

        fname = f"ThunderCats_{date_str}_{cat}_Report.pdf"
        if period == "Full Report":
            fname = f"ThunderCats_{date_str}_FULL_{cat}_Report.pdf"

        if os.path.exists(fname):
            timestamp = datetime.now().strftime("%H-%M-%S")
            fname = f"ThunderCats_{date_str}_{cat}_{timestamp}.pdf"


        start, end = self.get_date_range(period)
        if cat == "Sale":
            # New Detailed Columns
            table_data = self.db.salereportdb.fetch_sales_list(start, end)
            headers = ["Sale ID", "Product", "Category", "Unit Price", "Date", "Line Total", "Payment"]
        else:
            table_data = self.db.salereportdb.fetch_product_sales_list(start, end)
            headers = ["Product Name", "Category", "Qty Sold", "Total Revenue"]


        if self.generate_table_pdf(fname, headers, table_data, cat, period):
            #Save to DB & Refresh
            abs_path = os.path.abspath(fname)
            saved = self.db.salereportdb.add_generated_report(fname, abs_path, cat)
            if saved:
                self.load_reports_history()
                QMessageBox.information(self.ui, "Success", f"Report Generated!\nSaved to: {fname}")
            else:
                QMessageBox.warning(self.ui, "Warning", "PDF created but not saved to History.")

    def generate_table_pdf(self, filename, headers, data, report_type, period):
        try:
            doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
            elements = []
            styles = getSampleStyleSheet()

            title = Paragraph(f"ThunderCats POS - {report_type} Report", styles['Title'])
            elements.append(title)
            elements.append(Paragraph(f"Period: {period}", styles['Normal']))
            elements.append(Spacer(1, 20))

            pdf_data = [headers]
            total_sum = 0.0

            for row in data:
                row_list = list(row)
                if report_type == "Sale":
                    u_price = float(row_list[3]) if row_list[3] else 0.0
                    row_list[3] = f"P{u_price:,.2f}"

                    row_list[4] = str(row_list[4])

                    val = float(row_list[5]) if row_list[5] else 0.0
                    row_list[5] = f"P{val:,.2f}"

                    total_sum += val
                else:

                    val = float(row_list[3])
                    row_list[3] = f"P{val:,.2f}"
                    total_sum += val

                pdf_data.append(row_list)

            if report_type == "Sale":
                pdf_data.append(["", "", "", "", "GRAND TOTAL:", f"P{total_sum:,.2f}", ""])
            else:
                pdf_data.append(["", "", "TOTAL REVENUE:", f"P{total_sum:,.2f}"])

            table = Table(pdf_data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), pdf_colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), pdf_colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, pdf_colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
            ])
            table.setStyle(style)
            elements.append(table)

            doc.build(elements)
            return True

        except Exception as e:
            print(f"PDF Error: {e}")
            return False

    def load_reports_history(self):
        reports = self.db.salereportdb.fetch_all_reports()
        self.ui.table_reports.setRowCount(0)

        for row_idx, report in enumerate(reports):
            self.ui.table_reports.insertRow(row_idx)
            self.ui.table_reports.setItem(row_idx, 0, QTableWidgetItem(str(report['report_name'])))
            self.ui.table_reports.setItem(row_idx, 1, QTableWidgetItem(str(report['report_type'])))
            self.ui.table_reports.setItem(row_idx, 2, QTableWidgetItem(str(report['date_created'])))

            btn_open = QPushButton("Open")
            btn_open.setStyleSheet("background-color: #FFD500; color: black; font-weight: bold;")
            file_path = report['file_path']
            btn_open.clicked.connect(lambda checked, path=file_path: self.open_pdf(path))
            self.ui.table_reports.setCellWidget(row_idx, 3, btn_open)

    def open_pdf(self, file_path):
        if os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        else:
            QMessageBox.warning(self.ui, "Error", "File not found! It may have been moved or deleted.")