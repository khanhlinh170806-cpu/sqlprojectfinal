from models.db_config import get_connection

def get_all_orders():
    """Trả về tất cả đơn hàng JOIN với tên khách hàng"""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT o.Order_ID, c.Full_Name, o.Order_Date,
               o.Status, o.Total_Amount
        FROM Orders o
        JOIN Customers c ON o.Customer_ID = c.Customer_ID
        ORDER BY o.Order_Date DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_all_customers_for_dropdown():
    """Lấy danh sách khách hàng cho Combobox"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Customer_ID, Full_Name FROM Customers ORDER BY Full_Name")
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def add_order(customer_id, status, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Orders (Customer_ID, Status, Total_Amount)
           VALUES (%s, %s, %s)""",
        (customer_id, status, total_amount)
    )
    conn.commit()
    cursor.close(); conn.close()

def update_order(order_id, customer_id, status, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Orders
           SET Customer_ID=%s, Status=%s, Total_Amount=%s
           WHERE Order_ID=%s""",
        (customer_id, status, total_amount, order_id)
    )
    conn.commit()
    cursor.close(); conn.close()

def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders WHERE Order_ID=%s", (order_id,))
    conn.commit()
    cursor.close(); conn.close()

def search_orders(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT o.Order_ID, c.Full_Name, o.Order_Date,
               o.Status, o.Total_Amount
        FROM Orders o
        JOIN Customers c ON o.Customer_ID = c.Customer_ID
        WHERE c.Full_Name LIKE %s OR o.Status LIKE %s
        ORDER BY o.Order_Date DESC
    """
    like = f"%{keyword}%"
    cursor.execute(sql, (like, like))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result