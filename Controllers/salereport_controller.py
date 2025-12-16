from datetime import datetime, timedelta

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QVBoxLayout
from matplotlib import ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


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

        self.ui.combo_category.currentIndexChanged.connect(self.refresh_report)
        self.ui.combo_period.currentIndexChanged.connect(self.refresh_report)

        self.ui.date_start.setDate(QDate.currentDate())
        self.ui.date_end.setDate(QDate.currentDate())
        try:
            self.refresh_report()
        except Exception as e:
            print(f"Error during initial load: {e}")

    def load_chart_data(self, time_filter):

        start_date, end_date = self.get_date_range(time_filter)

        data = self.db.salereportdb.fetch_revenue_by_category(start_date, end_date)
        print(f"DEBUG: Date Range: {start_date} to {end_date}")
        print(f"DEBUG: Chart Data: {data}")
        self.plot_revenue_chart(data)

    def plot_revenue_chart(self, data):

        if self.canvas:
            self.chart_layout.removeWidget(self.canvas)
            self.canvas.close()
            self.canvas = None

        # Handle Empty Data
        if not data:

            return

        #Prepare Data with Pandas
        df = pd.DataFrame(data)
        categories = df['Category'].astype(str).tolist()
        revenue = df['Revenue'].astype(float).tolist()

        # Create the Figure ---
        fig = Figure(figsize=(5, 3), dpi=100)

        fig.patch.set_facecolor('#2A004E')

        ax = fig.add_subplot(111)
        ax.set_facecolor('#2A004E')

        # --- E. Draw the Bars ---
        bars = ax.bar(categories, revenue, color='#FFD500', width=0.6)

        # --- F. Styling the Text ---
        ax.tick_params(axis='x', colors='white', labelsize=9)
        ax.tick_params(axis='y', colors='white', labelsize=9)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            label_text = f"₱{height:,.2f}"
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    label_text,
                    ha='center', va='bottom', color='white', fontsize=8)

        #Add to GUI ---
        self.canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(self.canvas)

    def get_date_range(self, time_filter):
        now = datetime.now()

        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        if time_filter == "This Day":
            pass

        elif time_filter == "This Week":
            start_date = start_date - timedelta(days=start_date.weekday())

        elif time_filter == "This Month":
            start_date = start_date.replace(day=1)

        elif time_filter == "Full Report":
            start_date = start_date.replace(year=2000, month=1, day=1)

        return start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')

    def refresh_report(self):
        #Get Current Selections
        report_type = self.ui.combo_category.currentText()
        time_period = self.ui.combo_period.currentText()
        start, end = self.get_date_range(time_period)

        print(f"DEBUG: Querying {report_type} from [{start}] to [{end}]")

        stats = self.db.salereportdb.fetch_summary_stats(start, end)

        self.ui.lbl_revenue.setText(f"₱{stats['total_sales']:,.2f}")
        self.ui.lbl_ticket.setText(f"₱{stats['avg_ticket']:,.2f}")
        self.ui.lbl_category.setText(str(stats['top_category']))

        if report_type == "Sale":
            #Fetch Revenue Data (Money)
            data = self.db.salereportdb.fetch_revenue_by_category(start, end)
            self.ui.header_rev.setText("Revenue by Component")
            self.plot_graph(data, "Revenue")

        elif report_type == "Product":
            # Fetch Volume Data (Quantity Sold)
            data = self.db.salereportdb.fetch_top_products(start, end)
            self.ui.header_rev.setText("Top Selling Products (Qty)")
            self.plot_graph(data, "Quantity")

    def plot_graph(self, data, metric_name):

        self.figure.clear()

        if not data:
            print("No data to plot.")
            self.canvas.draw()
            return

        # Prepare Data
        df = pd.DataFrame(data)

        # Handle different column names
        if metric_name == "Revenue":
            if 'Category' not in df.columns: return  # Safety check
            labels = df['Category'].astype(str).tolist()
            values = df['Revenue'].astype(float).tolist()
            bar_color = '#FFD500'
        else:
            if 'product_name' not in df.columns: return  # Safety check
            labels = df['product_name'].astype(str).tolist()
            values = df['quantity'].astype(int).tolist()
            bar_color = '#00D4FF'

            # Add Subplot to the existing Figure
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#2A004E')
        self.figure.subplots_adjust(bottom=0.3)

        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        # Draw Bars
        bars = ax.bar(labels, values, color=bar_color, width=0.6)

        # Styling
        ax.tick_params(axis='x', colors='white', labelsize=8, rotation=15)
        ax.tick_params(axis='y', colors='white', labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        # Add Labels
        for bar in bars:
            height = bar.get_height()
            label_text = f"₱{height:,.2f}" if metric_name == "Revenue" else f"{int(height)}"
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    label_text,
                    ha='center', va='bottom', color='white', fontsize=8)


        self.canvas.draw()