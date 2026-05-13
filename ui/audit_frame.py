# ui/audit_frame.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

from models.audit import get_audit_logs, get_audit_logs_by_table

TABLE_FILTERS = ["Tất cả", "Orders", "Deliveries", "Expenses"]

class AuditFrame:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        # ── Thanh công cụ ─────────────────────────────────────
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill="x", padx=10, pady=10)

        ttk.Label(toolbar, text="🔐 Nhật Ký Truy Cập (Audit Log)",
                  font=("Helvetica", 12, "bold")).pack(side="left")

        ttk.Button(toolbar, text="↻ Làm mới",
                   bootstyle="secondary",
                   command=self.load_data).pack(side="right", padx=4)

        # Lọc theo bảng
        ttk.Label(toolbar, text="Lọc theo bảng:").pack(side="right", padx=(10, 4))
        self.filter_var = tk.StringVar(value="Tất cả")
        cb = ttk.Combobox(toolbar, textvariable=self.filter_var,
                          values=TABLE_FILTERS, state="readonly", width=14)
        cb.pack(side="right")
        cb.bind("<<ComboboxSelected>>", lambda e: self.load_data())

        # ── Thẻ tóm tắt ───────────────────────────────────────
        card_row = ttk.Frame(self.parent)
        card_row.pack(fill="x", padx=10, pady=(0, 8))

        self.card_total    = self._make_card(card_row, "Tổng log",   "0", "primary")
        self.card_update   = self._make_card(card_row, "UPDATE",     "0", "warning")
        self.card_insert   = self._make_card(card_row, "INSERT",     "0", "success")

        # ── Bảng log ──────────────────────────────────────────
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("Log ID", "Bảng", "Hành động", "Record ID",
                   "Người thực hiện", "Thời gian", "Giá trị cũ", "Giá trị mới")
        self.tree = ttk.Treeview(table_frame, columns=columns,
                                 show="headings", bootstyle="primary", height=22)

        widths = [60, 100, 90, 80, 160, 160, 220, 220]
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=60)

        # Màu theo loại hành động
        self.tree.tag_configure("UPDATE", background="#fff3cd")
        self.tree.tag_configure("INSERT", background="#d4edda")
        self.tree.tag_configure("DELETE", background="#f8d7da")

        sb_y = ttk.Scrollbar(table_frame, orient="vertical",
                             command=self.tree.yview)
        sb_x = ttk.Scrollbar(table_frame, orient="horizontal",
                             command=self.tree.xview)
        self.tree.configure(yscrollcommand=sb_y.set,
                            xscrollcommand=sb_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right",  fill="y")
        sb_x.pack(side="bottom", fill="x")

    def _make_card(self, parent, label, value, style):
        frame = ttk.Frame(parent, bootstyle=style, padding=(10, 6))
        frame.pack(side="left", padx=5)
        ttk.Label(frame, text=value,
                  font=("Helvetica", 16, "bold"),
                  bootstyle=f"inverse-{style}").pack()
        ttk.Label(frame, text=label,
                  font=("Helvetica", 9),
                  bootstyle=f"inverse-{style}").pack()
        # trả về label số để cập nhật sau
        return frame.winfo_children()[0]

    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        chosen = self.filter_var.get()
        if chosen == "Tất cả":
            rows = get_audit_logs(200)
        else:
            rows = get_audit_logs_by_table(chosen)

        for row in rows:
            action = str(row[2])
            self.tree.insert("", "end", values=row, tags=(action,))

        # Cập nhật thẻ tóm tắt
        total   = len(rows)
        updates = sum(1 for r in rows if r[2] == "UPDATE")
        inserts = sum(1 for r in rows if r[2] == "INSERT")

        self.card_total.config( text=str(total))
        self.card_update.config(text=str(updates))
        self.card_insert.config(text=str(inserts))