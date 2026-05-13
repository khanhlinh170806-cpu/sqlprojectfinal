USE delivery_system_v2026;

-- Thêm 2 cột lưu dữ liệu đã mã hoá
ALTER TABLE Customers
  ADD COLUMN Phone_Encrypted   VARBINARY(255) NULL,
  ADD COLUMN Address_Encrypted VARBINARY(255) NULL;

-- Mã hoá dữ liệu hiện có từ cột gốc
UPDATE Customers
SET
  Phone_Encrypted   = AES_ENCRYPT(Phone,   'DeliveryKey2026'),
  Address_Encrypted = AES_ENCRYPT(Address, 'DeliveryKey2026');

-- View giải mã: ứng dụng sẽ đọc từ view này thay vì bảng gốc
CREATE VIEW vw_customers_decrypted AS
SELECT
  Customer_ID,
  Full_Name,
  CAST(AES_DECRYPT(Phone_Encrypted,   'DeliveryKey2026') AS CHAR) AS Phone,
  CAST(AES_DECRYPT(Address_Encrypted, 'DeliveryKey2026') AS CHAR) AS Address,
  Created_At
FROM Customers;

-- Phân quyền: chỉ manager và dispatcher được xem
GRANT SELECT ON delivery_system_v2026.vw_customers_decrypted
  TO 'delivery_manager'@'localhost';
GRANT SELECT ON delivery_system_v2026.vw_customers_decrypted
  TO 'dispatcher'@'localhost';

FLUSH PRIVILEGES;