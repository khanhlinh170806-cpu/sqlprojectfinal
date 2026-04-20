from models.db_config import get_connection

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Customer_ID, Full_Name, Phone, Address
        FROM Customers
        ORDER BY Customer_ID DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def add_customer(name, phone, address, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Customers (Full_Name, Phone, Address) VALUES (%s, %s, %s)",
        (name, phone, address)
    )
    conn.commit()
    cursor.close(); conn.close()

def update_customer(customer_id, name, phone, address, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Customers SET Full_Name=%s, Phone=%s, Address=%s WHERE Customer_ID=%s",
        (name, phone, address, customer_id)
    )
    conn.commit()
    cursor.close(); conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE Customer_ID=%s", (customer_id,))
    conn.commit()
    cursor.close(); conn.close()

def search_customers(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like = f"%{keyword}%"
    cursor.execute("""
        SELECT Customer_ID, Full_Name, Phone, Address
        FROM Customers
        WHERE Full_Name LIKE %s OR Phone LIKE %s
    """, (like, like))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result