-- Tạo database mới với tên định danh riêng biệt
CREATE DATABASE IF NOT EXISTS delivery_system_v2026;
USE delivery_system_v2026;
-- =============================================================
-- File: 1_schema.sql
-- Project: DELIVERY SERVICE MANAGEMENT SYSTEM
-- Description: Database Schema for Project 10
-- =============================================================

-- 1. Bảng Customers: Lưu thông tin khách hàng
CREATE TABLE IF NOT EXISTS Customers (
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL UNIQUE,
    Address TEXT NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng Orders: Quản lý các đơn đặt hàng
CREATE TABLE IF NOT EXISTS Orders (
    Order_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Order_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('Pending', 'Confirmed', 'Shipping', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    Total_Amount DECIMAL(15, 2) NOT NULL,

    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID) ON DELETE CASCADE
);

-- 3. Bảng Vehicles: Quản lý đội xe vận chuyển
CREATE TABLE IF NOT EXISTS Vehicles (
    Vehicle_ID INT AUTO_INCREMENT PRIMARY KEY,
    Plate_Number VARCHAR(20) NOT NULL UNIQUE,
    Vehicle_Type VARCHAR(50) NOT NULL,
    Availability BOOLEAN DEFAULT TRUE,
    Last_Maintenance DATE
);

-- 4. Bảng Deliveries: Phân công giao hàng và theo dõi trạng thái
CREATE TABLE IF NOT EXISTS Deliveries (
    Delivery_ID INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID INT NOT NULL UNIQUE, -- Mỗi đơn hàng gắn với 1 chuyến giao
    Vehicle_ID INT NOT NULL,
    Estimated_Time DATETIME,
    Delivery_Status ENUM('In Transit', 'Completed', 'Failed') DEFAULT 'In Transit',
    Driver_Note VARCHAR(255) NOT NULL,
    CONSTRAINT chk_driver_note CHECK (Driver_Note IN (
        'Handle with care', 
        'Gate code 1234', 
        'Call before arrival'
    )),
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID) ON DELETE CASCADE
);

-- 5. Bảng Expenses: Theo dõi chi phí phát sinh cho mỗi chuyến giao
CREATE TABLE IF NOT EXISTS Expenses (
    Expense_ID INT AUTO_INCREMENT PRIMARY KEY,
    Delivery_ID INT NOT NULL,
    Expense_Type ENUM('Fuel', 'Toll Fee', 'Parking', 'Loading', 'Other') NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,
    Recorded_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Delivery_ID) REFERENCES Deliveries(Delivery_ID) ON DELETE CASCADE
);