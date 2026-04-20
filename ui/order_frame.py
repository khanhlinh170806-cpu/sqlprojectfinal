import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk

from models.order import (
    get_all_orders,
    get_all_customers_for_dropdown,
    add_order,
    update_order,
    delete_order,
    search_orders
)

STATUS_OPTIONS = ['Pending', 'Confirmed', 'Shipping', 'Delivered', 'Cancelled']

class OrderFrame:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.customer_map = {}   # {Full_Name: Customer_ID}

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        left  = ttk.Frame(self.parent, width=320)
        right = ttk.Frame(self.parent)
        left.pack(side="left", fill="y", padx=10, pady=10)
        right.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        left.pack_propagate(False)

        self._build_form(left)
        self._build_table(right)

    # ── FORM ─────────────────────────────────────────────────
    def _build_form(self, parent):
        ttk.Label(parent, text="Thông Tin Đơn Hàng",
                  font=("Helvetica", 12, "bold")).pack(pady=(0, 10))

        # Khách hàng — Combobox
        ttk.Label(parent, text="Khách Hàng").pack(anchor="w")
        self.customer_var = tk.StringVar()
        self.customer_cb = ttk.Combobox(parent, textvariable=self.customer_var,
                                        state="readonly", width=33)
        self.customer_cb.pack(fill="x", pady=(0, 8))

        # Trạng thái — Combobox
        ttk.Label(parent, text="Trạng Thái").pack(anchor="w")
        self.status_var = tk.StringVar(value="Pending")
        self.status_cb = ttk.Combobox(parent, textvariable=self.status_var,
                                      values=STATUS_OPTIONS, state="readonly", width=33)
        self.status_cb.pack(fill="x", pady=(0, 8))

        # Tổng tiền
        ttk.Label(parent, text="Tổng Tiền (VNĐ)").pack(anchor="w")
        self.amount_entry = ttk.Entry(parent, width=35)
        self.amount_entry.pack(fill="x", pady=(0, 8))

        # Nút bấm
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(btn_frame, text="➕ Thêm",    bootstyle="success",
                   command=self.add_record).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="✏️ Sửa",     bootstyle="warning",
                   command=self.update_record).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="🗑️ Xóa",     bootstyle="danger",
                   command=self.delete_record).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="🔄 Làm Mới", bootstyle="secondary",
                   command=self.clear_form).pack(side="left", padx=3)

        # Nút refresh danh sách khách hàng
        ttk.Button(parent, text="↻ Tải lại danh sách khách hàng",
                   bootstyle="info-outline",
                   command=self.load_customers).pack(fill="x", pady=(5, 0))

        self.load_customers()

    def load_customers(self):
        """Nạp danh sách khách hàng vào combobox"""
        customers = get_all_customers_for_dropdown()
        self.customer_map = {name: cid for cid, name in customers}
        self.customer_cb["values"] = list(self.customer_map.keys())

    # ── BẢNG ─────────────────────────────────────────────────
    def _build_table(self, parent):
        # Thanh tìm kiếm
        sf = ttk.Frame(parent)
        sf.pack(fill="x", pady=(0, 8))
        ttk.Label(sf, text="🔍 Tìm kiếm:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.search())
        ttk.Entry(sf, textvariable=self.search_var, width=30).pack(side="left", padx=5)
        ttk.Button(sf, text="↻ Tải lại", bootstyle="secondary-outline",
                   command=self.load_data).pack(side="right")

        # Treeview
        columns = ("ID", "Khách Hàng", "Ngày Đặt", "Trạng Thái", "Tổng Tiền")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings",
                                 bootstyle="primary", height=22)
        col_widths = [50, 200, 160, 120, 150]
        for col, w in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ── XỬ LÝ SỰ KIỆN ────────────────────────────────────────
    def load_data(self, data=None):
        self.tree.delete(*self.tree.get_children())
        rows = data if data is not None else get_all_orders()
        for row in rows:
            # Format tiền tệ
            formatted = list(row)
            try:
                formatted[4] = f"{float(row[4]):,.0f} đ"
            except (ValueError, TypeError, IndexError):
                pass
            self.tree.insert("", "end", values=formatted)

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        self.selected_id = values[0]

        # Điền vào form
        self.customer_var.set(values[1])
        self.status_var.set(values[3])

        # Xóa format tiền để có thể edit
        amount_raw = str(values[4]).replace(",", "").replace(" đ", "").replace("đ", "").strip()
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, amount_raw)

    def _get_customer_id(self):
        name = self.customer_var.get()
        return self.customer_map.get(name)

    def add_record(self):
        cid = self._get_customer_id()
        status = self.status_var.get()
        amount = self.amount_entry.get().strip()

        if not cid:
            Messagebox.show_warning("Vui lòng chọn khách hàng!", "Thiếu thông tin")
            return
        if not amount:
            Messagebox.show_warning("Vui lòng nhập tổng tiền!", "Thiếu thông tin")
            return
        try:
            amount = float(amount)
        except ValueError:
            Messagebox.show_warning("Tổng tiền phải là số!", "Lỗi dữ liệu")
            return

        add_order(cid, status, amount)
        Messagebox.show_info("Thêm đơn hàng thành công!", "Thành công")
        self.clear_form()
        self.load_data()

    def update_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần sửa!", "Chưa chọn")
            return
        cid = self._get_customer_id()
        status = self.status_var.get()
        amount = self.amount_entry.get().strip()

        if not cid:
            Messagebox.show_warning("Vui lòng chọn khách hàng!", "Thiếu thông tin")
            return
        try:
            amount = float(amount)
        except ValueError:
            Messagebox.show_warning("Tổng tiền phải là số!", "Lỗi dữ liệu")
            return

        update_order(self.selected_id, cid, status, amount)
        Messagebox.show_info("Cập nhật thành công!", "Thành công")
        self.clear_form()
        self.load_data()

    def delete_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần xóa!", "Chưa chọn")
            return
        confirm = Messagebox.yesno("Bạn có chắc muốn xóa đơn hàng này không?", "Xác nhận xóa")
        if confirm == "Yes":
            delete_order(self.selected_id)
            self.clear_form()
            self.load_data()

    def clear_form(self):
        self.selected_id = None
        self.customer_var.set("")
        self.status_var.set("Pending")
        self.amount_entry.delete(0, "end")

    def search(self):
        keyword = self.search_var.get()
        if keyword:
            filtered = search_orders(keyword)
            self.load_data(filtered)
        else:
            self.load_data()