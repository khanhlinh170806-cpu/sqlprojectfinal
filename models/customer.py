# models/customer.py
from models.db_config import get_connection

ENCRYPT_KEY = 'DeliveryKey2026'   # phải khớp với key trong SQL


def get_all_customers():
    """Đọc từ view — Phone và Address đã được giải mã tự động"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Customer_ID, Full_Name, Phone, Address
        FROM vw_customers_decrypted
        ORDER BY Customer_ID DESC
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result


def add_customer(name, phone, address, **kwargs):
    """Ghi Phone và Address dưới dạng mã hoá vào cột _Encrypted"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Customers
             (Full_Name, Phone, Address,
              Phone_Encrypted, Address_Encrypted)
           VALUES (
             %s,
             %s,
             %s,
             AES_ENCRYPT(%s, %s),
             AES_ENCRYPT(%s, %s)
           )""",
        (name, phone, address,
         phone,   ENCRYPT_KEY,
         address, ENCRYPT_KEY)
    )
    conn.commit()
    cursor.close(); conn.close()


def update_customer(customer_id, name, phone, address, **kwargs):
    """Cập nhật cả cột gốc lẫn cột mã hoá"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Customers
           SET Full_Name         = %s,
               Phone             = %s,
               Address           = %s,
               Phone_Encrypted   = AES_ENCRYPT(%s, %s),
               Address_Encrypted = AES_ENCRYPT(%s, %s)
           WHERE Customer_ID = %s""",
        (name, phone, address,
         phone,   ENCRYPT_KEY,
         address, ENCRYPT_KEY,
         customer_id)
    )
    conn.commit()
    cursor.close(); conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM Customers WHERE Customer_ID=%s",
        (customer_id,)
    )
    conn.commit()
    cursor.close(); conn.close()


def search_customers(keyword):
    """Tìm kiếm qua view (dữ liệu đã giải mã)"""
    conn = get_connection()
    cursor = conn.cursor()
    like = f"%{keyword}%"
    cursor.execute("""
        SELECT Customer_ID, Full_Name, Phone, Address
        FROM vw_customers_decrypted
        WHERE Full_Name LIKE %s OR Phone LIKE %s
    """, (like, like))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result