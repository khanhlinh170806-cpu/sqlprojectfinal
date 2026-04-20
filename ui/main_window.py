# ui/main_window.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ui.customer_frame import CustomerFrame
from ui.order_frame import OrderFrame
from ui.delivery_frame import DeliveryFrame
from ui.report_frame import ReportFrame

class MainWindow:
    def __init__(self):
        # Tạo cửa sổ chính với theme hiện đại
        self.root = ttk.Window(
            title="Delivery Service Management System",
            themename="cosmo",   # Có thể đổi: flatly, journal, darkly...
            size=(1200, 700),
            resizable=(True, True)
        )

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        """Thanh tiêu đề phía trên"""
        header = ttk.Frame(self.root, bootstyle="primary")
        header.pack(fill="x", pady=(0, 5))

        ttk.Label(
            header,
            text="🚚  Delivery Service Management System",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-primary"
        ).pack(side="left", padx=20, pady=10)

    def _build_tabs(self):
        """Tạo hệ thống tab điều hướng"""
        notebook = ttk.Notebook(self.root, bootstyle="primary")
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tạo từng tab và truyền notebook vào để dùng chung
        tabs = [
            ("👥 Khách Hàng",  CustomerFrame),
            ("📦 Đơn Hàng",    OrderFrame),
            ("🚗 Giao Hàng",   DeliveryFrame),
            ("📊 Báo Cáo",     ReportFrame),
        ]

        for tab_name, FrameClass in tabs:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=tab_name)
            FrameClass(frame)   # Khởi tạo nội dung từng tab

    def run(self):
        self.root.mainloop()