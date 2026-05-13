# models/expense.py
from models.db_config import get_connection

def get_expenses_by_delivery(delivery_id):
    """Lấy tất cả chi phí của một chuyến giao hàng"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Expense_ID, Expense_Type, Amount, Recorded_At
           FROM Expenses
           WHERE Delivery_ID = %s
           ORDER BY Recorded_At""",
        (delivery_id,)
    )
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def add_expense(delivery_id, expense_type, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Expenses (Delivery_ID, Expense_Type, Amount)
           VALUES (%s, %s, %s)""",
        (delivery_id, expense_type, amount)
    )
    conn.commit()
    cursor.close(); conn.close()

def get_all_deliveries_for_dropdown():
    """Lấy danh sách delivery để chọn khi thêm chi phí"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT d.Delivery_ID, o.Order_ID, c.Full_Name
           FROM Deliveries d
           JOIN Orders o ON d.Order_ID = o.Order_ID
           JOIN Customers c ON o.Customer_ID = c.Customer_ID
           ORDER BY d.Delivery_ID DESC"""
    )
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result