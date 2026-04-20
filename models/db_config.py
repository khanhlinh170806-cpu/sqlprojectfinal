import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="linhzhuminh.123",
        database="delivery_system_v2026"
    )