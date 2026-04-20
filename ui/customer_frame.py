import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk

from models.customer import (
    get_all_customers,
    add_customer,
    update_customer,
    delete_customer,
    search_customers
)

class CustomerFrame:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None

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
        ttk.Label(parent, text="Thông Tin Khách Hàng",
                  font=("Helvetica", 12, "bold")).pack(pady=(0, 10))

        self.entries = {}
        fields = [
            ("Họ và Tên *", "name"),
            ("Số Điện Thoại *", "phone"),
            ("Địa Chỉ", "address"),
        ]

        for label_text, key in fields:
            ttk.Label(parent, text=label_text).pack(anchor="w")
            entry = ttk.Entry(parent, width=35)
            entry.pack(fill="x", pady=(0, 8))
            self.entries[key] = entry

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

    # ── BẢNG ─────────────────────────────────────────────────
    def _build_table(self, parent):
        sf = ttk.Frame(parent)
        sf.pack(fill="x", pady=(0, 8))
        ttk.Label(sf, text="🔍 Tìm kiếm:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.search())
        ttk.Entry(sf, textvariable=self.search_var, width=30).pack(side="left", padx=5)
        ttk.Button(sf, text="↻ Tải lại", bootstyle="secondary-outline",
                   command=self.load_data).pack(side="right")

        # Schema không có email → chỉ 4 cột
        columns = ("ID", "Họ Tên", "SĐT", "Địa Chỉ")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings",
                                 bootstyle="primary", height=22)

        col_widths = [60, 220, 140, 350]
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
        rows = data if data is not None else get_all_customers()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        self.selected_id = values[0]

        keys = ["name", "phone", "address"]
        for i, key in enumerate(keys):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, values[i + 1])

    def add_record(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if not data["name"] or not data["phone"]:
            Messagebox.show_warning("Vui lòng nhập Họ Tên và SĐT!", "Thiếu thông tin")
            return
        add_customer(**data)
        Messagebox.show_info("Thêm khách hàng thành công!", "Thành công")
        self.clear_form()
        self.load_data()

    def update_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần sửa!", "Chưa chọn")
            return
        data = {k: e.get().strip() for k, e in self.entries.items()}
        update_customer(self.selected_id, **data)
        Messagebox.show_info("Cập nhật thành công!", "Thành công")
        self.clear_form()
        self.load_data()

    def delete_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần xóa!", "Chưa chọn")
            return
        confirm = Messagebox.yesno("Bạn có chắc muốn xóa khách hàng này không?", "Xác nhận xóa")
        if confirm == "Yes":
            delete_customer(self.selected_id)
            self.clear_form()
            self.load_data()

    def clear_form(self):
        self.selected_id = None
        for entry in self.entries.values():
            entry.delete(0, "end")

    def search(self):
        keyword = self.search_var.get()
        if keyword:
            filtered = search_customers(keyword)
            self.load_data(filtered)
        else:
            self.load_data()