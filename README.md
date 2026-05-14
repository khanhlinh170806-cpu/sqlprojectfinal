# Delivery Service Management System

A relational database-driven application for managing logistics and delivery operations, built with **MySQL 8.0** and **Python 3.13 (Tkinter GUI)**.

> Final Project — National Economics University, College of Technology  
> Author: Le Pham Khanh Linh | Class: DSEB 66B | Supervisor: Tran Hung | Hanoi, 2026

---

## ️ Demo

-  **YouTube Demo:** https://www.youtube.com/@khanhlinhlepham4259
-  **Presentation Slides:** https://byvn.net/L13C

---

##  Project Overview

This system automates core delivery operations including customer management, order lifecycle tracking, vehicle assignment, expense logging, and operational reporting. It integrates advanced database features with a role-based access control model to support real-world logistics workflows.

---

## ️ Project Structure

```
sqlprojectfinal/
│
├── main.py                   # Entry point
├── ui/
│   ├── main_window.py        # MainWindow — Tkinter root with navigation tabs
│   ├── customer_frame.py
│   ├── order_frame.py
│   ├── delivery_frame.py
│   ├── invoice_frame.py
│   ├── report_frame.py
│   └── audit_frame.py
│
├── models/
│   ├── customer.py           # CRUD for Customers table
│   ├── order.py              # CRUD for Orders table
│   ├── vehicle.py            # Vehicle availability queries
│   ├── delivery.py           # Delivery assignment & status updates
│   └── expense.py            # Expense insertion & queries
│
├── 1_schema.sql              # CREATE TABLE for all 5 tables
├── 2_mock_data.sql           # Sample INSERT data for testing
├── 3_advanced_objects.sql    # Indexes, Views, Stored Procedures, UDFs, Trigger
├── 4_security_roles.sql      # CREATE USER and GRANT statements
├── backup_script.bat         # Automated mysqldump backup (Windows)
└── README.md
```

---

## ️ Technology Stack

| Component | Technology |
|---|---|
| Database | MySQL 8.0 |
| Programming Language | Python 3.13 |
| DB Connector | mysql-connector-python |
| GUI Framework | Tkinter + ttkbootstrap |
| ER Design Tool | MySQL Workbench |
| Version Control | Git / GitHub |

---

##  Getting Started

### Prerequisites

- Python 3.13+
- MySQL 8.0+
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/khanhlinh170806-cpu/sqlprojectfinal
cd sqlprojectfinal
```

**2. Install Python dependencies**

```bash
pip install mysql-connector-python ttkbootstrap python-dotenv
```

**3. Set up the database**

Open MySQL Workbench or your MySQL client and run the SQL files in order:

```sql
source 1_schema.sql;
source 2_mock_data.sql;
source 3_advanced_objects.sql;
source 4_security_roles.sql;
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```
DB_HOST=localhost
DB_USER=delivery_manager
DB_PASSWORD=Manager@123
DB_NAME=delivery_system_v2026
```

**5. Run the application**

```bash
python main.py
```

---

## ️ Database Schema

The database `delivery_system_v2026` consists of five normalized tables:

| Table | Description |
|---|---|
| `Customers` | Customer profiles — name, phone, address |
| `Vehicles` | Fleet info — plate number, type, availability |
| `Orders` | Customer orders with status lifecycle |
| `Deliveries` | Links orders to vehicles; tracks delivery status |
| `Expenses` | Per-delivery operational costs (fuel, toll, etc.) |

**Order Status Lifecycle:**
```
Pending → Confirmed → Shipping → Delivered / Cancelled
```

**Delivery Status:**
```
In Transit → Completed / Failed
```

---

##  Advanced Database Features

### Indexes
- `idx_orders_status` — fast filtering by order status
- `idx_vehicles_availability` — quick lookup of available vehicles
- `idx_deliveries_status` — optimised active delivery queries
- `idx_orders_customer` — efficient cost aggregation per customer

### Views
| View | Purpose |
|---|---|
| `vw_active_deliveries` | All deliveries currently In Transit |
| `vw_cost_per_order` | Total expense aggregated per order |
| `vw_backlog_orders` | Pending orders unresolved for 30+ days |

### Stored Procedures
| Procedure | Description |
|---|---|
| `sp_assign_vehicle(order_id, vehicle_id)` | Checks availability, creates delivery, updates order status atomically |
| `sp_monthly_expenses(month, year)` | Groups expenses by type for a given month |

### User-Defined Functions
| Function | Returns |
|---|---|
| `fn_avg_delivery_cost()` | Average cost across all deliveries |
| `fn_order_count_by_vehicle(vehicle_id)` | Total deliveries handled by a vehicle |

### Trigger
- `trg_update_order_on_delivery` — automatically sets `Orders.Status = 'Delivered'` when a delivery is marked `Completed`

---

##  User Roles & Permissions

| Permission | Manager | Dispatcher | Accountant |
|---|:---:|:---:|:---:|
| SELECT all tables |  |  |  |
| INSERT / UPDATE Orders |  |  |  |
| INSERT / UPDATE Deliveries |  |  |  |
| INSERT / UPDATE Expenses |  |  |  |
| CALL stored procedures |  |  (assign only) |  |
| CREATE / DROP objects |  |  |  |
| GRANT / REVOKE users |  |  |  |

---

## ️ Application Tabs

| Tab | Description |
|---|---|
| **Khách Hàng** (Customers) | Add, search, and manage customer profiles |
| **Đơn Hàng** (Orders) | Create and update orders through their lifecycle |
| **Giao Hàng** (Deliveries) | Assign vehicles and track delivery status |
| **Hóa Đơn** (Invoices) | View and export order invoices |
| **Báo Cáo** (Reports) | Monthly expenses, cost per order, backlog reports |
| **Audit Log** | Track all INSERT/UPDATE activity with timestamps |

---

##  Security

- **Role-Based Access Control (RBAC):** least-privilege model with three distinct MySQL user roles
- **SQL Injection Prevention:** all queries use parameterised `%s` placeholders
- **Credential Management:** database credentials stored in `.env`, never hardcoded
- **Password Hashing:** MySQL users created with `caching_sha2_password`

---

##  Backup & Recovery

**Automated Backup (Windows):**
```bash
# Run manually or schedule via Windows Task Scheduler
backup_script.bat
# Generates: backup_YYYYMMDD_HHMMSS.sql
```

**Recovery:**
```sql
CREATE DATABASE delivery_system_v2026;
USE delivery_system_v2026;
-- Then restore via CLI:
-- mysql -u root -p delivery_system_v2026 < backup_YYYYMMDD_HHMMSS.sql
```

---

##  Testing

Key scenarios validated during development:

-  Assigning an unavailable vehicle raises `SQLSTATE 45000` and rolls back
-  Duplicate phone numbers rejected by `UNIQUE` constraint
-  Invalid ENUM values blocked at database schema level
-  Trigger correctly syncs order status to `Delivered` on delivery completion
-  Tkinter UI validates empty fields and non-numeric inputs before DB calls

---

##  Future Development

- ️ **GPS Integration** — real-time tracking via Google Maps API
-  **Mobile App** — Android/iOS for drivers to update status remotely
-  **Notifications** — SMS/email via Twilio or SendGrid
-  **Web Dashboard** — Flask + Chart.js for graphical KPI monitoring
-  **Payment Gateway** — COD and electronic payment tracking
-  **Customer Rating System** — delivery quality feedback

---

##  References

1. MySQL 8.0 Reference Manual — https://dev.mysql.com/doc/refman/8.0/en/
2. Python Documentation — https://docs.python.org/3/
3. mysql-connector-python Guide — https://dev.mysql.com/doc/connector-python/en/

---

##  License

This project was developed for academic purposes at National Economics University, Hanoi.
