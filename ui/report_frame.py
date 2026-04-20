import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

from models.report import (
    get_delivery_performance,
    get_order_summary,
    get_expense_summary,
    get_vehicle_stats,
    get_top_customers
)

class ReportFrame:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()
        # Tự động load báo cáo đầu tiên khi mở tab
        self.show_report("delivery")

    def _build_ui(self):
        # ── Thanh nút chọn báo cáo ───────────────────────────
        btn_bar = ttk.Frame(self.parent, bootstyle="light")
        btn_bar.pack(fill="x", padx=10, pady=10)

        ttk.Label(btn_bar, text="📊 Chọn báo cáo:",
                  font=("Helvetica", 11, "bold")).pack(side="left", padx=(0, 10))

        reports = [
            ("🚚 Hiệu Suất Giao Hàng",  "delivery"),
            ("📦 Tóm Tắt Đơn Hàng",     "order"),
            ("💰 Chi Phí",               "expense"),
            ("🚗 Thống Kê Xe",           "vehicle"),
            ("👥 Top Khách Hàng",        "customer"),
        ]

        for label, key in reports:
            ttk.Button(btn_bar, text=label, bootstyle="primary-outline",
                       command=lambda k=key: self.show_report(k)
                       ).pack(side="left", padx=4)

        ttk.Button(btn_bar, text="↻ Làm Mới", bootstyle="secondary",
                   command=self.refresh).pack(side="right", padx=4)

        # ── Tiêu đề báo cáo hiện tại ─────────────────────────
        self.report_title = ttk.Label(
            self.parent, text="", font=("Helvetica", 13, "bold")
        )
        self.report_title.pack(padx=10, pady=(0, 5), anchor="w")

        # ── Tóm tắt nhanh (summary cards) ────────────────────
        self.summary_frame = ttk.Frame(self.parent)
        self.summary_frame.pack(fill="x", padx=10, pady=(0, 8))

        # ── Bảng dữ liệu ─────────────────────────────────────
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(table_frame, show="headings",
                                 bootstyle="primary", height=20)
        sb_y = ttk.Scrollbar(table_frame, orient="vertical",   command=self.tree.yview)
        sb_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right",  fill="y")
        sb_x.pack(side="bottom", fill="x")

        self.current_report = "delivery"

    # ── HIỂN THỊ TỪNG BÁO CÁO ────────────────────────────────
    def show_report(self, report_key):
        self.current_report = report_key
        self.tree.delete(*self.tree.get_children())

        # Xóa summary cards cũ
        for w in self.summary_frame.winfo_children():
            w.destroy()

        if report_key == "delivery":
            self._show_delivery_performance()
        elif report_key == "order":
            self._show_order_summary()
        elif report_key == "expense":
            self._show_expense_summary()
        elif report_key == "vehicle":
            self._show_vehicle_stats()
        elif report_key == "customer":
            self._show_top_customers()

    def refresh(self):
        self.show_report(self.current_report)

    # ── BÁO CÁO 1: Hiệu suất giao hàng ──────────────────────
    def _show_delivery_performance(self):
        self.report_title.config(text="🚚 Báo Cáo Hiệu Suất Giao Hàng")
        data = get_delivery_performance()

        cols = ("Trạng Thái", "Số Lượng", "Tỉ Lệ (%)")
        self._set_columns(cols, [160, 120, 120])

        total = sum(row[1] for row in data)
        self._add_summary_cards([
            ("Tổng chuyến", str(total), "primary"),
            ("Hoàn thành",  str(next((r[1] for r in data if r[0]=="Completed"), 0)), "success"),
            ("Thất bại",    str(next((r[1] for r in data if r[0]=="Failed"),    0)), "danger"),
        ])

        color_map = {"Completed": "success", "Failed": "danger", "In Transit": "warning"}
        for row in data:
            tag = color_map.get(str(row[0]), "")
            self.tree.insert("", "end", values=row, tags=(tag,))

        self.tree.tag_configure("success", background="#d4edda")
        self.tree.tag_configure("danger",  background="#f8d7da")
        self.tree.tag_configure("warning", background="#fff3cd")

    # ── BÁO CÁO 2: Tóm tắt đơn hàng ─────────────────────────
    def _show_order_summary(self):
        self.report_title.config(text="📦 Báo Cáo Tóm Tắt Đơn Hàng")
        data = get_order_summary()

        cols = ("Trạng Thái", "Số Đơn", "Doanh Thu (đ)")
        self._set_columns(cols, [160, 120, 200])

        total_orders  = sum(r[1] for r in data)
        total_revenue = sum(float(r[2]) for r in data if r[2])
        self._add_summary_cards([
            ("Tổng đơn hàng", str(total_orders), "primary"),
            ("Tổng doanh thu", f"{total_revenue:,.0f} đ", "success"),
            ("Đang chờ", str(next((r[1] for r in data if r[0]=="Pending"), 0)), "warning"),
        ])

        for row in data:
            formatted = list(row)
            try:
                formatted[2] = f"{float(row[2]):,.0f} đ"
            except (ValueError, TypeError):
                pass
            self.tree.insert("", "end", values=formatted)

    # ── BÁO CÁO 3: Chi phí ───────────────────────────────────
    def _show_expense_summary(self):
        self.report_title.config(text="💰 Báo Cáo Chi Phí Theo Loại")
        data = get_expense_summary()

        cols = ("Loại Chi Phí", "Số Lần", "Tổng Chi Phí (đ)", "Trung Bình (đ)")
        self._set_columns(cols, [160, 100, 200, 200])

        total_exp = sum(float(r[2]) for r in data if r[2])
        self._add_summary_cards([
            ("Tổng chi phí", f"{total_exp:,.0f} đ", "danger"),
            ("Loại chi phí", str(len(data)), "info"),
        ])

        for row in data:
            formatted = list(row)
            try:
                formatted[2] = f"{float(row[2]):,.0f} đ"
                formatted[3] = f"{float(row[3]):,.0f} đ"
            except (ValueError, TypeError):
                pass
            self.tree.insert("", "end", values=formatted)

    # ── BÁO CÁO 4: Thống kê xe ───────────────────────────────
    def _show_vehicle_stats(self):
        self.report_title.config(text="🚗 Thống Kê Xe Theo Số Chuyến Giao")
        data = get_vehicle_stats()

        cols = ("Biển Số", "Loại Xe", "Tổng Chuyến", "Hoàn Thành", "Thất Bại")
        self._set_columns(cols, [130, 150, 120, 120, 100])

        total_vehicles = len(data)
        active = sum(1 for r in data if r[2] and int(r[2]) > 0)
        self._add_summary_cards([
            ("Tổng số xe",  str(total_vehicles), "primary"),
            ("Xe đã hoạt động", str(active),     "success"),
        ])

        for row in data:
            self.tree.insert("", "end", values=row)

    # ── BÁO CÁO 5: Top khách hàng ────────────────────────────
    def _show_top_customers(self):
        self.report_title.config(text="👥 Top 10 Khách Hàng Theo Doanh Thu")
        data = get_top_customers()

        cols = ("Khách Hàng", "Số Đơn", "Tổng Chi Tiêu (đ)")
        self._set_columns(cols, [220, 100, 200])

        self._add_summary_cards([
            ("Top khách hàng", data[0][0] if data else "—", "success"),
            ("Chi tiêu cao nhất", f"{float(data[0][2]):,.0f} đ" if data else "—", "primary"),
        ])

        for i, row in enumerate(data):
            formatted = list(row)
            try:
                formatted[2] = f"{float(row[2]):,.0f} đ"
            except (ValueError, TypeError):
                pass
            medal = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
            formatted[0] = f"{medal} {formatted[0]}"
            self.tree.insert("", "end", values=formatted)

    # ── HELPER ───────────────────────────────────────────────
    def _set_columns(self, columns, widths):
        """Cấu hình lại cột cho Treeview"""
        self.tree["columns"] = columns
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=80)

    def _add_summary_cards(self, cards):
        """Tạo các thẻ tóm tắt phía trên bảng"""
        for label, value, style in cards:
            card = ttk.Frame(self.summary_frame, bootstyle=f"{style}", padding=8)
            card.pack(side="left", padx=5, pady=2)
            ttk.Label(card, text=value,
                      font=("Helvetica", 14, "bold"),
                      bootstyle=f"inverse-{style}").pack()
            ttk.Label(card, text=label,
                      font=("Helvetica", 9),
                      bootstyle=f"inverse-{style}").pack()