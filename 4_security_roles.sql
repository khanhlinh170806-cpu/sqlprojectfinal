-- Bước 1: Tạo users trước
CREATE USER 'delivery_manager'@'localhost' IDENTIFIED BY 'Manager@123';
CREATE USER 'dispatcher'@'localhost' IDENTIFIED BY 'Dispatch@123';
CREATE USER 'accountant'@'localhost' IDENTIFIED BY 'Account@123';
-- bước 2: 
GRANT ALL PRIVILEGES ON delivery_system_v2026.* TO 'delivery_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE ON delivery_system_v2026.Orders TO 'dispatcher'@'localhost';
GRANT SELECT, INSERT, UPDATE ON delivery_system_v2026.Deliveries TO 'dispatcher'@'localhost';
GRANT SELECT ON delivery_system_v2026.Vehicles TO 'dispatcher'@'localhost';
GRANT SELECT ON delivery_system_v2026.Customers TO 'dispatcher'@'localhost';
GRANT SELECT, INSERT, UPDATE ON delivery_system_v2026.Expenses TO 'accountant'@'localhost';
GRANT SELECT ON delivery_system_v2026.Orders TO 'accountant'@'localhost';
GRANT SELECT ON delivery_system_v2026.Deliveries TO 'accountant'@'localhost';

FLUSH PRIVILEGES;