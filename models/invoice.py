# models/invoice.py
from models.db_config import get_connection
from datetime import datetime

def get_invoice_data(order_id: int) -> dict:
    """
    Lấy toàn bộ dữ liệu cần thiết để tạo hóa đơn cho một Order.
    Trả về dict hoặc None nếu không tìm thấy.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Thông tin đơn hàng + khách hàng
    cursor.execute("""
        SELECT
            o.Order_ID,
            o.Order_Date,
            o.Status,
            o.Total_Amount,
            c.Full_Name     AS Customer_Name,
            c.Phone         AS Customer_Phone,
            c.Address       AS Customer_Address
        FROM Orders o
        JOIN Customers c ON o.Customer_ID = c.Customer_ID
        WHERE o.Order_ID = %s
    """, (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close(); conn.close()
        return None

    # 2. Thông tin giao hàng + xe
    cursor.execute("""
        SELECT
            d.Delivery_ID,
            d.Estimated_Time,
            d.Delivery_Status,
            d.Driver_Note,
            v.Plate_Number,
            v.Vehicle_Type
        FROM Deliveries d
        JOIN Vehicles v ON d.Vehicle_ID = v.Vehicle_ID
        WHERE d.Order_ID = %s
    """, (order_id,))
    delivery = cursor.fetchone()

    # 3. Chi phí (nếu có delivery)
    expenses = []
    total_expense = 0.0
    if delivery:
        cursor.execute("""
            SELECT Expense_Type, Amount, Recorded_At
            FROM Expenses
            WHERE Delivery_ID = %s
            ORDER BY Recorded_At
        """, (delivery['Delivery_ID'],))
        expenses = cursor.fetchall()
        total_expense = sum(float(e['Amount']) for e in expenses)

    cursor.close(); conn.close()

    return {
        'invoice_number': f"INV-{order_id:05d}",
        'generated_at':   datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'order':          order,
        'delivery':       delivery,
        'expenses':       expenses,
        'total_expense':  total_expense,
        'grand_total':    float(order['Total_Amount']) + total_expense
    }

def get_all_order_ids():
    """Lấy danh sách Order ID để hiển thị trong combobox"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.Order_ID, c.Full_Name, o.Status
        FROM Orders o
        JOIN Customers c ON o.Customer_ID = c.Customer_ID
        ORDER BY o.Order_ID DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result