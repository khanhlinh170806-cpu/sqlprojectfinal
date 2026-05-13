# ui/invoice_frame.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from tkinter import filedialog
import os

from models.invoice import get_invoice_data, get_all_order_ids

class InvoiceFrame:
    def __init__(self, parent):
        self.parent   = parent
        self.order_map = {}   # {"#1 - customer1 (Delivered)": 1, ...}
        self.current_invoice = None

        self._build_ui()
        self.load_order_list()

    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        # Chia layout: trái (chọn đơn) | phải (xem hóa đơn)
        left = ttk.Frame(self.parent, width=280)
        left.pack(side="left", fill="y", padx=10, pady=10)
        left.pack_propagate(False)

        right = ttk.Frame(self.parent)
        right.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        self._build_selector(left)
        self._build_preview(right)

    # ── Panel trái: chọn đơn hàng ────────────────────────────
    def _build_selector(self, parent):
        ttk.Label(parent, text="Xuất Hóa Đơn",
                  font=("Helvetica", 12, "bold")).pack(pady=(0, 12))

        ttk.Label(parent, text="Chọn đơn hàng:").pack(anchor="w")
        self.order_var = tk.StringVar()
        self.order_cb = ttk.Combobox(
            parent, textvariable=self.order_var,
            state="readonly", width=32
        )
        self.order_cb.pack(fill="x", pady=(0, 10))

        ttk.Button(
            parent, text="🔍 Xem Hóa Đơn",
            bootstyle="primary", width=28,
            command=self.show_invoice
        ).pack(fill="x", pady=3)

        ttk.Button(
            parent, text="💾 Lưu File .txt",
            bootstyle="success-outline", width=28,
            command=self.save_invoice
        ).pack(fill="x", pady=3)

        ttk.Button(
            parent, text="↻ Tải lại danh sách",
            bootstyle="secondary-outline", width=28,
            command=self.load_order_list
        ).pack(fill="x", pady=(10, 3))

        # Thẻ tóm tắt (hiển thị sau khi tạo hóa đơn)
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=12)
        ttk.Label(parent, text="Tóm tắt",
                  font=("Helvetica", 10, "bold")).pack(anchor="w")

        self.card_order   = self._make_card(parent, "Mã đơn hàng", "—", "primary")
        self.card_status  = self._make_card(parent, "Trạng thái",  "—", "info")
        self.card_total   = self._make_card(parent, "Tổng cộng",   "—", "success")
        self.card_expense = self._make_card(parent, "Chi phí PS",  "—", "warning")

    def _make_card(self, parent, label, value, style):
        frame = ttk.Frame(parent, bootstyle=style, padding=(8, 5))
        frame.pack(fill="x", pady=3)
        ttk.Label(frame, text=label,
                  font=("Helvetica", 8),
                  bootstyle=f"inverse-{style}").pack(anchor="w")
        lbl = ttk.Label(frame, text=value,
                        font=("Helvetica", 12, "bold"),
                        bootstyle=f"inverse-{style}")
        lbl.pack(anchor="w")
        return lbl   # trả về label để cập nhật sau

    # ── Panel phải: hiển thị nội dung hóa đơn ────────────────
    def _build_preview(self, parent):
        ttk.Label(parent, text="Nội Dung Hóa Đơn",
                  font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

        # Text widget với scrollbar
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True)

        self.text_box = tk.Text(
            text_frame,
            font=("Courier New", 11),
            wrap="none",
            bg="#f8f9fa",
            fg="#212529",
            relief="flat",
            padx=12, pady=10
        )
        sb_y = ttk.Scrollbar(text_frame, orient="vertical",
                             command=self.text_box.yview)
        sb_x = ttk.Scrollbar(text_frame, orient="horizontal",
                             command=self.text_box.xview)
        self.text_box.configure(
            yscrollcommand=sb_y.set,
            xscrollcommand=sb_x.set
        )

        self.text_box.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")

        # Placeholder
        self._set_text("Chọn đơn hàng ở bên trái và nhấn '🔍 Xem Hóa Đơn'")

    # ── Logic chính ───────────────────────────────────────────
    def load_order_list(self):
        orders = get_all_order_ids()
        self.order_map = {
            f"#{oid} — {name} ({status})": oid
            for oid, name, status in orders
        }
        self.order_cb["values"] = list(self.order_map.keys())

    def show_invoice(self):
        key = self.order_var.get()
        if not key:
            Messagebox.show_warning("Vui lòng chọn đơn hàng!", "Chưa chọn")
            return

        order_id = self.order_map.get(key)
        data = get_invoice_data(order_id)

        if not data:
            Messagebox.show_error(
                f"Không tìm thấy dữ liệu cho đơn hàng #{order_id}!", "Lỗi"
            )
            return

        self.current_invoice = data
        text = self._format_invoice(data)
        self._set_text(text)
        self._update_cards(data)

    def save_invoice(self):
        if not self.current_invoice:
            Messagebox.show_warning("Vui lòng xem hóa đơn trước khi lưu!", "Chưa có dữ liệu")
            return

        inv_num = self.current_invoice['invoice_number']
        default_name = f"{inv_num}.txt"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_name,
            title="Lưu hóa đơn"
        )

        if filepath:
            content = self._format_invoice(self.current_invoice)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            Messagebox.show_info(
                f"Đã lưu hóa đơn tại:\n{filepath}", "Lưu thành công"
            )

    # ── Định dạng hóa đơn thành chuỗi văn bản ────────────────
    def _format_invoice(self, data: dict) -> str:
        SEP  = "=" * 58
        THIN = "-" * 58

        lines = [
            SEP,
            "         HÓA ĐƠN DỊCH VỤ GIAO HÀNG",
            f"  Số hóa đơn : {data['invoice_number']}",
            f"  Ngày xuất  : {data['generated_at']}",
            SEP,
        ]

        # Thông tin khách hàng
        o = data['order']
        lines += [
            "  THÔNG TIN KHÁCH HÀNG",
            THIN,
            f"  Họ và tên  : {o['Customer_Name']}",
            f"  Số ĐT      : {o['Customer_Phone']}",
            f"  Địa chỉ    : {o['Customer_Address']}",
            THIN,
        ]

        # Thông tin đơn hàng
        lines += [
            "  THÔNG TIN ĐƠN HÀNG",
            THIN,
            f"  Mã đơn     : #{o['Order_ID']}",
            f"  Ngày đặt   : {o['Order_Date']}",
            f"  Trạng thái : {o['Status']}",
            f"  Giá trị ĐH : {float(o['Total_Amount']):>12,.0f} VNĐ",
            THIN,
        ]

        # Thông tin giao hàng
        d = data['delivery']
        if d:
            lines += [
                "  THÔNG TIN GIAO HÀNG",
                THIN,
                f"  Mã giao    : #D{d['Delivery_ID']}",
                f"  Phương tiện: {d['Vehicle_Type']} — {d['Plate_Number']}",
                f"  Dự kiến GT : {d['Estimated_Time']}",
                f"  Trạng thái : {d['Delivery_Status']}",
                f"  Ghi chú    : {d['Driver_Note']}",
                THIN,
            ]
        else:
            lines += ["  ⚠  Đơn hàng này chưa được phân công giao hàng.", THIN]

        # Chi phí phát sinh
        if data['expenses']:
            lines += ["  CHI PHÍ PHÁT SINH", THIN]
            for exp in data['expenses']:
                lines.append(
                    f"  {str(exp['Expense_Type']):<22}"
                    f"{float(exp['Amount']):>12,.0f} VNĐ"
                )
            lines.append(THIN)
        else:
            lines += ["  (Không có chi phí phát sinh)", THIN]

        # Tổng kết
        lines += [
            f"  Giá trị đơn hàng     : {float(o['Total_Amount']):>12,.0f} VNĐ",
            f"  Tổng chi phí phát sinh: {data['total_expense']:>11,.0f} VNĐ",
            SEP,
            f"  TỔNG CỘNG THANH TOÁN : {data['grand_total']:>12,.0f} VNĐ",
            SEP,
            "",
            "  Cảm ơn quý khách đã sử dụng dịch vụ!",
            SEP,
        ]

        return "\n".join(lines)

    # ── Helper ────────────────────────────────────────────────
    def _set_text(self, content: str):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", content)
        self.text_box.config(state="disabled")

    def _update_cards(self, data: dict):
        o = data['order']
        self.card_order.config(  text=f"#{o['Order_ID']}")
        self.card_status.config( text=o['Status'])
        self.card_total.config(  text=f"{data['grand_total']:,.0f} đ")
        self.card_expense.config(text=f"{data['total_expense']:,.0f} đ")