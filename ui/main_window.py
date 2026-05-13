
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ui.customer_frame  import CustomerFrame
from ui.order_frame     import OrderFrame
from ui.delivery_frame  import DeliveryFrame
from ui.report_frame    import ReportFrame
from ui.invoice_frame   import InvoiceFrame   
from ui.audit_frame     import AuditFrame     

class MainWindow:
    def __init__(self):
        self.root = ttk.Window(
            title="Delivery Service Management System",
            themename="cosmo",
            size=(1280, 720),
            resizable=(True, True)
        )
        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header = ttk.Frame(self.root, bootstyle="primary")
        header.pack(fill="x", pady=(0, 5))
        ttk.Label(
            header,
            text="🚚  Delivery Service Management System",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-primary"
        ).pack(side="left", padx=20, pady=10)

    def _build_tabs(self):
        notebook = ttk.Notebook(self.root, bootstyle="primary")
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        tabs = [
            ("👥 Khách Hàng",  CustomerFrame),
            ("📦 Đơn Hàng",    OrderFrame),
            ("🚗 Giao Hàng",   DeliveryFrame),
            ("🧾 Hóa Đơn",     InvoiceFrame),
            ("📊 Báo Cáo",     ReportFrame),
            ("🔐 Audit Log",   AuditFrame),   
        ]

        for tab_name, FrameClass in tabs:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=tab_name)
            FrameClass(frame)

    def run(self):
        self.root.mainloop()