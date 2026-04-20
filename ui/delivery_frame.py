import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from datetime import datetime

from models.delivery import (
    get_all_deliveries,
    get_orders_for_dropdown,
    get_vehicles_for_dropdown,
    add_delivery,
    update_delivery,
    delete_delivery,
    search_deliveries
)

STATUS_OPTIONS  = ['In Transit', 'Completed', 'Failed']
DRIVER_NOTES    = ['Handle with care', 'Gate code 1234', 'Call before arrival']

class DeliveryFrame:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id    = None
        self.order_map   = {}   # {display_text: order_id}
        self.vehicle_map = {}   # {display_text: vehicle_id}

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        left  = ttk.Frame(self.parent, width=340)
        right = ttk.Frame(self.parent)
        left.pack(side="left", fill="y", padx=10, pady=10)
        right.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        left.pack_propagate(False)

        self._build_form(left)
        self._build_table(right)

    # ── FORM ─────────────────────────────────────────────────
    def _build_form(self, parent):
        ttk.Label(parent, text="Thông Tin Giao Hàng",
                  font=("Helvetica", 12, "bold")).pack(pady=(0, 10))

        # Đơn hàng — Combobox
        ttk.Label(parent, text="Đơn Hàng (ID - Khách hàng)").pack(anchor="w")
        self.order_var = tk.StringVar()
        self.order_cb = ttk.Combobox(parent, textvariable=self.order_var,
                                     state="readonly", width=35)
        self.order_cb.pack(fill="x", pady=(0, 8))

        # Xe — Combobox
        ttk.Label(parent, text="Phương Tiện (Biển số - Loại xe)").pack(anchor="w")
        self.vehicle_var = tk.StringVar()
        self.vehicle_cb = ttk.Combobox(parent, textvariable=self.vehicle_var,
                                       state="readonly", width=35)
        self.vehicle_cb.pack(fill="x", pady=(0, 8))

        # Thời gian dự kiến
        ttk.Label(parent, text="Thời Gian Dự Kiến (YYYY-MM-DD HH:MM)").pack(anchor="w")
        self.time_entry = ttk.Entry(parent, width=35)
        self.time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.time_entry.pack(fill="x", pady=(0, 8))

        # Trạng thái giao hàng
        ttk.Label(parent, text="Trạng Thái Giao Hàng").pack(anchor="w")
        self.status_var = tk.StringVar(value="In Transit")
        self.status_cb = ttk.Combobox(parent, textvariable=self.status_var,
                                      values=STATUS_OPTIONS, state="readonly", width=35)
        self.status_cb.pack(fill="x", pady=(0, 8))

        # Ghi chú tài xế
        ttk.Label(parent, text="Ghi Chú Tài Xế").pack(anchor="w")
        self.note_var = tk.StringVar(value=DRIVER_NOTES[0])
        self.note_cb = ttk.Combobox(parent, textvariable=self.note_var,
                                    values=DRIVER_NOTES, state="readonly", width=35)
        self.note_cb.pack(fill="x", pady=(0, 8))

        # Nút bấm
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="➕ Thêm",    bootstyle="success",
                   command=self.add_record).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="✏️ Sửa",     bootstyle="warning",
                   command=self.update_record).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🗑️ Xóa",     bootstyle="danger",
                   command=self.delete_record).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🔄 Làm Mới", bootstyle="secondary",
                   command=self.clear_form).pack(side="left", padx=2)

        ttk.Button(parent, text="↻ Tải lại danh sách đơn hàng & xe",
                   bootstyle="info-outline",
                   command=self.load_dropdowns).pack(fill="x", pady=(5, 0))

        self.load_dropdowns()

    def load_dropdowns(self):
        """Nạp danh sách đơn hàng và xe vào combobox"""
        orders = get_orders_for_dropdown()
        self.order_map = {f"#{oid} - {name} ({status})": oid
                          for oid, name, status in orders}
        self.order_cb["values"] = list(self.order_map.keys())

        vehicles = get_vehicles_for_dropdown()
        self.vehicle_map = {f"{plate} ({vtype})": vid
                            for vid, plate, vtype in vehicles}
        self.vehicle_cb["values"] = list(self.vehicle_map.keys())

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

        columns = ("ID", "Đơn Hàng #", "Biển Số", "Thời Gian DK", "Trạng Thái", "Ghi Chú")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings",
                                 bootstyle="primary", height=22)
        col_widths = [50, 90, 110, 160, 110, 200]
        for col, w in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        # Màu dòng theo trạng thái
        self.tree.tag_configure("completed", background="#d4edda")
        self.tree.tag_configure("failed",    background="#f8d7da")
        self.tree.tag_configure("transit",   background="#fff3cd")

        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ── XỬ LÝ SỰ KIỆN ────────────────────────────────────────
    def load_data(self, data=None):
        self.tree.delete(*self.tree.get_children())
        rows = data if data is not None else get_all_deliveries()
        for row in rows:
            status = str(row[4]) if len(row) > 4 else ""
            tag = ("completed" if status == "Completed"
                   else "failed" if status == "Failed"
                   else "transit")
            self.tree.insert("", "end", values=row, tags=(tag,))

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        self.selected_id = values[0]

        # Tìm key trong order_map theo order_id (values[1])
        for key, oid in self.order_map.items():
            if str(oid) == str(values[1]):
                self.order_var.set(key)
                break

        # Tìm key trong vehicle_map theo plate number (values[2])
        for key in self.vehicle_map:
            if str(values[2]) in key:
                self.vehicle_var.set(key)
                break

        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, str(values[3]))
        self.status_var.set(values[4])
        self.note_var.set(values[5])

    def _get_vehicle_id(self):
        return self.vehicle_map.get(self.vehicle_var.get())

    def _validate_time(self, time_str):
        try:
            datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def add_record(self):
        order_key   = self.order_var.get()
        vehicle_id  = self._get_vehicle_id()
        time_str    = self.time_entry.get().strip()
        status      = self.status_var.get()
        note        = self.note_var.get()

        order_id = self.order_map.get(order_key)

        if not order_id:
            Messagebox.show_warning("Vui lòng chọn đơn hàng!", "Thiếu thông tin")
            return
        if not vehicle_id:
            Messagebox.show_warning("Vui lòng chọn phương tiện!", "Thiếu thông tin")
            return
        if not self._validate_time(time_str):
            Messagebox.show_warning("Định dạng thời gian phải là YYYY-MM-DD HH:MM", "Lỗi định dạng")
            return

        add_delivery(order_id, vehicle_id, time_str, status, note)
        Messagebox.show_info("Phân công giao hàng thành công!", "Thành công")
        self.clear_form()
        self.load_data()
        self.load_dropdowns()

    def update_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần sửa!", "Chưa chọn")
            return
        vehicle_id = self._get_vehicle_id()
        time_str   = self.time_entry.get().strip()
        status     = self.status_var.get()
        note       = self.note_var.get()

        if not vehicle_id:
            Messagebox.show_warning("Vui lòng chọn phương tiện!", "Thiếu thông tin")
            return
        if not self._validate_time(time_str):
            Messagebox.show_warning("Định dạng thời gian phải là YYYY-MM-DD HH:MM", "Lỗi định dạng")
            return

        update_delivery(self.selected_id, vehicle_id, time_str, status, note)
        Messagebox.show_info("Cập nhật thành công!", "Thành công")
        self.clear_form()
        self.load_data()

    def delete_record(self):
        if not self.selected_id:
            Messagebox.show_warning("Vui lòng chọn dòng cần xóa!", "Chưa chọn")
            return
        confirm = Messagebox.yesno("Bạn có chắc muốn xóa chuyến giao hàng này không?", "Xác nhận xóa")
        if confirm == "Yes":
            delete_delivery(self.selected_id)
            self.clear_form()
            self.load_data()
            self.load_dropdowns()

    def clear_form(self):
        self.selected_id = None
        self.order_var.set("")
        self.vehicle_var.set("")
        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.status_var.set("In Transit")
        self.note_var.set(DRIVER_NOTES[0])

    def search(self):
        keyword = self.search_var.get()
        if keyword:
            filtered = search_deliveries(keyword)
            self.load_data(filtered)
        else:
            self.load_data()