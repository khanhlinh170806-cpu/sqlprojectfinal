from models.db_config import get_connection

def get_all_deliveries():
    """Trả về tất cả deliveries JOIN với Orders và Vehicles"""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT d.Delivery_ID, d.Order_ID, v.Plate_Number,
               d.Estimated_Time, d.Delivery_Status, d.Driver_Note
        FROM Deliveries d
        JOIN Orders   o ON d.Order_ID   = o.Order_ID
        JOIN Vehicles v ON d.Vehicle_ID = v.Vehicle_ID
        ORDER BY d.Delivery_ID DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_orders_for_dropdown():
    """Chỉ lấy đơn hàng chưa có delivery để tránh trùng (UNIQUE constraint)"""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT o.Order_ID, c.Full_Name, o.Status
        FROM Orders o
        JOIN Customers c ON o.Customer_ID = c.Customer_ID
        WHERE o.Order_ID NOT IN (SELECT Order_ID FROM Deliveries)
        ORDER BY o.Order_ID DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_vehicles_for_dropdown():
    """Chỉ lấy xe đang available"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Vehicle_ID, Plate_Number, Vehicle_Type FROM Vehicles WHERE Availability=TRUE"
    )
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def add_delivery(order_id, vehicle_id, estimated_time, delivery_status, driver_note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Deliveries (Order_ID, Vehicle_ID, Estimated_Time, Delivery_Status, Driver_Note)
           VALUES (%s, %s, %s, %s, %s)""",
        (order_id, vehicle_id, estimated_time, delivery_status, driver_note)
    )
    conn.commit()
    cursor.close(); conn.close()

def update_delivery(delivery_id, vehicle_id, estimated_time, delivery_status, driver_note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Deliveries
           SET Vehicle_ID=%s, Estimated_Time=%s, Delivery_Status=%s, Driver_Note=%s
           WHERE Delivery_ID=%s""",
        (vehicle_id, estimated_time, delivery_status, driver_note, delivery_id)
    )
    conn.commit()
    cursor.close(); conn.close()

def delete_delivery(delivery_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Deliveries WHERE Delivery_ID=%s", (delivery_id,))
    conn.commit()
    cursor.close(); conn.close()

def search_deliveries(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT d.Delivery_ID, d.Order_ID, v.Plate_Number,
               d.Estimated_Time, d.Delivery_Status, d.Driver_Note
        FROM Deliveries d
        JOIN Orders   o ON d.Order_ID   = o.Order_ID
        JOIN Vehicles v ON d.Vehicle_ID = v.Vehicle_ID
        WHERE v.Plate_Number LIKE %s OR d.Delivery_Status LIKE %s OR d.Driver_Note LIKE %s
    """
    like = f"%{keyword}%"
    cursor.execute(sql, (like, like, like))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result