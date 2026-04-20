from models.db_config import get_connection

def get_delivery_performance():
    """Báo cáo hiệu suất giao hàng theo trạng thái"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Delivery_Status,
            COUNT(*) AS Total,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Deliveries), 1) AS Percentage
        FROM Deliveries
        GROUP BY Delivery_Status
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_order_summary():
    """Tóm tắt đơn hàng theo trạng thái"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Status,
            COUNT(*) AS Total_Orders,
            SUM(Total_Amount) AS Revenue
        FROM Orders
        GROUP BY Status
        ORDER BY Total_Orders DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_expense_summary():
    """Tóm tắt chi phí theo loại"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Expense_Type,
            COUNT(*) AS Count,
            SUM(Amount) AS Total_Amount,
            AVG(Amount) AS Avg_Amount
        FROM Expenses
        GROUP BY Expense_Type
        ORDER BY Total_Amount DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_vehicle_stats():
    """Thống kê số đơn hàng mỗi xe đã giao"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.Plate_Number,
            v.Vehicle_Type,
            COUNT(d.Delivery_ID) AS Total_Deliveries,
            SUM(CASE WHEN d.Delivery_Status='Completed' THEN 1 ELSE 0 END) AS Completed,
            SUM(CASE WHEN d.Delivery_Status='Failed'    THEN 1 ELSE 0 END) AS Failed
        FROM Vehicles v
        LEFT JOIN Deliveries d ON v.Vehicle_ID = d.Vehicle_ID
        GROUP BY v.Vehicle_ID, v.Plate_Number, v.Vehicle_Type
        ORDER BY Total_Deliveries DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_top_customers():
    """Top khách hàng theo doanh thu"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.Full_Name,
            COUNT(o.Order_ID) AS Total_Orders,
            SUM(o.Total_Amount) AS Total_Spent
        FROM Customers c
        JOIN Orders o ON c.Customer_ID = o.Customer_ID
        GROUP BY c.Customer_ID, c.Full_Name
        ORDER BY Total_Spent DESC
        LIMIT 10
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result