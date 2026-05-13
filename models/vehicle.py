# models/vehicle.py
from models.db_config import get_connection

def get_all_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT Vehicle_ID, Plate_Number, Vehicle_Type,
                  Availability, Last_Maintenance
           FROM Vehicles
           ORDER BY Vehicle_ID"""
    )
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

def add_vehicle(plate_number, vehicle_type, availability, last_maintenance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Vehicles (Plate_Number, Vehicle_Type, Availability, Last_Maintenance)
           VALUES (%s, %s, %s, %s)""",
        (plate_number, vehicle_type, availability, last_maintenance)
    )
    conn.commit()
    cursor.close(); conn.close()

def update_vehicle(vehicle_id, plate_number, vehicle_type, availability, last_maintenance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Vehicles
           SET Plate_Number=%s, Vehicle_Type=%s, Availability=%s, Last_Maintenance=%s
           WHERE Vehicle_ID=%s""",
        (plate_number, vehicle_type, availability, last_maintenance, vehicle_id)
    )
    conn.commit()
    cursor.close(); conn.close()

def delete_vehicle(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vehicles WHERE Vehicle_ID=%s", (vehicle_id,))
    conn.commit()
    cursor.close(); conn.close()

def search_vehicles(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like = f"%{keyword}%"
    cursor.execute(
        """SELECT Vehicle_ID, Plate_Number, Vehicle_Type, Availability, Last_Maintenance
           FROM Vehicles
           WHERE Plate_Number LIKE %s OR Vehicle_Type LIKE %s""",
        (like, like)
    )
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result