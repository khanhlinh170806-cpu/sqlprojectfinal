# models/audit.py
from models.db_config import get_connection

def get_audit_logs(limit=200):
    """Lấy log gần nhất, mặc định 200 dòng"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Log_ID, Table_Name, Action_Type,
               Record_ID, Changed_By, Changed_At,
               Old_Value, New_Value
        FROM Audit_Log
        ORDER BY Changed_At DESC
        LIMIT %s
    """, (limit,))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def get_audit_logs_by_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Log_ID, Table_Name, Action_Type,
               Record_ID, Changed_By, Changed_At,
               Old_Value, New_Value
        FROM Audit_Log
        WHERE Table_Name = %s
        ORDER BY Changed_At DESC
        LIMIT 200
    """, (table_name,))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result