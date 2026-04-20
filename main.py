from models import customer, order, vehicle, delivery, expense, report

def main_menu():
    while True:
        print("\n===== DELIVERY MANAGEMENT SYSTEM =====")
        print("1. Quản lý Khách hàng")
        print("2. Quản lý Đơn hàng")
        print("3. Quản lý Phương tiện")
        print("4. Phân công Giao hàng")
        print("5. Ghi nhận Chi phí")
        print("6. Báo cáo")
        print("0. Thoát")
        choice = input("Chọn: ")
        if choice == "1": customer.menu()
        elif choice == "2": order.menu()
        # ...
        elif choice == "0": break

if __name__ == "__main__":
    main_menu()