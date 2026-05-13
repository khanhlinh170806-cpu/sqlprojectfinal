USE delivery_system_v2026;

-- ============================================================
-- BẢNG GHI LOG: lưu mọi thay đổi quan trọng
-- ============================================================
CREATE TABLE IF NOT EXISTS Audit_Log (
  Log_ID      INT AUTO_INCREMENT PRIMARY KEY,
  Table_Name  VARCHAR(50)                    NOT NULL,
  Action_Type ENUM('INSERT','UPDATE','DELETE') NOT NULL,
  Record_ID   INT                            NOT NULL,
  Changed_By  VARCHAR(100)                   NOT NULL
              DEFAULT (CURRENT_USER()),
  Changed_At  TIMESTAMP                      DEFAULT CURRENT_TIMESTAMP,
  Old_Value   TEXT,
  New_Value   TEXT
);

-- ============================================================
-- TRIGGER 1: ghi log khi Orders thay đổi trạng thái
-- ============================================================
DELIMITER $$
CREATE TRIGGER trg_audit_orders_update
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
  IF OLD.Status <> NEW.Status OR OLD.Total_Amount <> NEW.Total_Amount THEN
    INSERT INTO Audit_Log
      (Table_Name, Action_Type, Record_ID, Old_Value, New_Value)
    VALUES (
      'Orders',
      'UPDATE',
      NEW.Order_ID,
      CONCAT('Status=', OLD.Status, ' | Amount=', OLD.Total_Amount),
      CONCAT('Status=', NEW.Status, ' | Amount=', NEW.Total_Amount)
    );
  END IF;
END$$
DELIMITER ;

-- ============================================================
-- TRIGGER 2: ghi log khi Expenses được thêm mới
-- ============================================================
DELIMITER $$
CREATE TRIGGER trg_audit_expenses_insert
AFTER INSERT ON Expenses
FOR EACH ROW
BEGIN
  INSERT INTO Audit_Log
    (Table_Name, Action_Type, Record_ID, New_Value)
  VALUES (
    'Expenses',
    'INSERT',
    NEW.Expense_ID,
    CONCAT('DeliveryID=', NEW.Delivery_ID,
           ' | Type=', NEW.Expense_Type,
           ' | Amount=', NEW.Amount)
  );
END$$
DELIMITER ;

-- ============================================================
-- TRIGGER 3: ghi log khi Deliveries đổi trạng thái
-- ============================================================
DELIMITER $$
CREATE TRIGGER trg_audit_delivery_update
AFTER UPDATE ON Deliveries
FOR EACH ROW
BEGIN
  IF OLD.Delivery_Status <> NEW.Delivery_Status THEN
    INSERT INTO Audit_Log
      (Table_Name, Action_Type, Record_ID, Old_Value, New_Value)
    VALUES (
      'Deliveries',
      'UPDATE',
      NEW.Delivery_ID,
      CONCAT('Status=', OLD.Delivery_Status),
      CONCAT('Status=', NEW.Delivery_Status)
    );
  END IF;
END$$
DELIMITER ;

-- ============================================================
-- Chỉ delivery_manager được xem Audit_Log
-- ============================================================
GRANT SELECT ON delivery_system_v2026.Audit_Log
  TO 'delivery_manager'@'localhost';

FLUSH PRIVILEGES;