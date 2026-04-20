-- index
CREATE INDEX idx_orders_status ON Orders(`Status`);
CREATE INDEX idx_vehicles_availability ON Vehicles(`Availability`);
CREATE INDEX idx_deliveries_status ON Deliveries(`Delivery_Status`);
CREATE INDEX idx_orders_customer ON Orders(Customer_ID);
-- view
-- View 1: Lịch giao hàng hiện tại
CREATE VIEW vw_active_deliveries AS
SELECT d.Delivery_ID, o.Order_ID, c.Full_Name, c.Phone,
       v.Plate_Number, v.Vehicle_Type,
       d.Estimated_Time, d.Delivery_Status, d.Driver_Note
FROM Deliveries d
JOIN Orders o ON d.Order_ID = o.Order_ID
JOIN Customers c ON o.Customer_ID = c.Customer_ID
JOIN Vehicles v ON d.Vehicle_ID = v.Vehicle_ID
WHERE d.Delivery_Status = 'In Transit';

-- View 2: Chi phí trên mỗi đơn hàng
CREATE VIEW vw_cost_per_order AS
SELECT o.Order_ID, c.Full_Name,
       SUM(e.Amount) AS Total_Expense
FROM Orders o
JOIN Deliveries d ON o.Order_ID = d.Order_ID
JOIN Expenses e ON d.Delivery_ID = e.Delivery_ID
JOIN Customers c ON o.Customer_ID = c.Customer_ID
GROUP BY o.Order_ID, c.Full_Name;

-- View 3: Đơn hàng tồn đọng (Pending quá 30 ngày)
CREATE VIEW vw_backlog_orders AS
SELECT o.Order_ID, c.Full_Name, o.Order_Date, o.Status,
       DATEDIFF(NOW(), o.Order_Date) AS Days_Pending
FROM Orders o
JOIN Customers c ON o.Customer_ID = c.Customer_ID
WHERE o.Status = 'Pending'
  AND DATEDIFF(NOW(), o.Order_Date) > 30
ORDER BY Days_Pending DESC;

-- stored procedures
-- SP 1: Phân công xe cho đơn hàng
DELIMITER $$
CREATE PROCEDURE sp_assign_vehicle(
    IN p_order_id INT,
    IN p_vehicle_id INT
)
BEGIN
    DECLARE v_available INT;
    SELECT Availability INTO v_available
    FROM Vehicles WHERE Vehicle_ID = p_vehicle_id;

    IF v_available = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Vehicle is not available!';
    ELSE
        INSERT INTO Deliveries (Order_ID, Vehicle_ID, Estimated_Time, Delivery_Status, Driver_Note)
        VALUES (p_order_id, p_vehicle_id, DATE_ADD(NOW(), INTERVAL 3 DAY), 'In Transit', 'Auto-assigned');
        UPDATE Vehicles SET Availability = 0 WHERE Vehicle_ID = p_vehicle_id;
        UPDATE Orders SET Status = 'Shipping' WHERE Order_ID = p_order_id;
    END IF;
END$$
DELIMITER ;

-- SP 2: Tổng chi phí theo tháng
DELIMITER $$
CREATE PROCEDURE sp_monthly_expenses(IN p_month INT, IN p_year INT)
BEGIN
    SELECT e.Expense_Type,
           COUNT(*) AS Count,
           SUM(e.Amount) AS Total_Amount
    FROM Expenses e
    JOIN Deliveries d ON e.Delivery_ID = d.Delivery_ID
    WHERE MONTH(d.Estimated_Time) = p_month
      AND YEAR(d.Estimated_Time) = p_year
    GROUP BY e.Expense_Type;
END$$
DELIMITER ;

-- user defined function
-- UDF 1: Chi phí giao hàng trung bình
DELIMITER $$
CREATE FUNCTION fn_avg_delivery_cost()
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE avg_cost DECIMAL(15,2);
    SELECT AVG(total) INTO avg_cost
    FROM (SELECT SUM(Amount) AS total FROM Expenses GROUP BY Delivery_ID) t;
    RETURN avg_cost;
END$$
DELIMITER ;

-- UDF 2: Số đơn hàng của một xe
DELIMITER $$
CREATE FUNCTION fn_order_count_by_vehicle(p_vehicle_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt FROM Deliveries WHERE Vehicle_ID = p_vehicle_id;
    RETURN cnt;
END$$
DELIMITER ;

-- trigger
DELIMITER $$
CREATE TRIGGER trg_update_order_on_delivery
AFTER UPDATE ON Deliveries
FOR EACH ROW
BEGIN
    IF NEW.Delivery_Status = 'Completed' THEN
        UPDATE Orders SET Status = 'Delivered'
        WHERE Order_ID = NEW.Order_ID;
    END IF;
END$$
DELIMITER ;

