import logging

logging.basicConfig(
    filename="roster_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

roster_db = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched"
    }
]

def calculate_actual_pay(player: dict) -> float:
    if "status" not in player or "salary" not in player:
        raise KeyError("Missing essential data keys: 'status' or 'salary'")
        
    if player["status"] == "Benched":
        return player["salary"] * 0.5
    return player["salary"]


def display_roster(roster_list: list) -> None:
    if not roster_list:
        print("\nĐội hình hiện đang trống.")
        return

 
    print(f"{'ID':<8} | {'Tên tuyển thủ':<20} | {'Vị trí':<15} | {'Lương':<12} | Trạng thái")
    print("-" * 80)
    
    for player in roster_list:
        status = player.get("status", "Unknown")
        player_id = player.get("player_id", "N/A")
        role = player.get("role", "N/A")
        salary = player.get("salary", 0.0)
        
        display_name = player.get("name", "Unknown")
        if status == "Benched":
            display_name += " [DỰ BỊ]"
            
        print(f"{player_id:<8} | {display_name:<20} | {role:<15} | {salary:?<12,s}".replace('?', '').replace('s', '').format(salary) if isinstance(salary, (int, float)) else f"{salary:<12}")
        print(f"{player_id:<8} | {display_name:<20} | {role:<15} | {salary:,.1f:<12} | {status}")
        
    print("-" * 80)
    logging.info("Coach viewed the team roster.")


def sign_player(roster_list: list) -> None:
    print("\n--- CHIÊU MỘ TUYỂN THỦ MỚI ---")
    
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    if not player_id:
        print("Mã tuyển thủ không được để trống.")
        return

    for player in roster_list:
        if player.get("player_id") == player_id:
            print(f"\nLỗi: Mã tuyển thủ {player_id} đã tồn tại.")
            logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
            return

    name = input("Nhập tên tuyển thủ: ").strip()
    role = input("Nhập vị trí thi đấu: ").strip()
    
    while True:
        try:
            salary_input = input("Nhập mức lương hàng tháng: ").strip()
            salary = float(salary_input)
            if salary <= 0:
                print("\nLương phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("\nLương phải là số. Vui lòng nhập lại.")
            logging.warning("Failed to sign player - Invalid salary input")

    new_player = {
        "player_id": player_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    }
    roster_list.append(new_player)
    print(f"\nThành công: Đã chiêu mộ tuyển thủ {name.title()}.")
    logging.info(f"Signed new player {name.title()} with salary {salary:.1f}")


def update_player_status(roster_list: list) -> None:
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")
    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()
    
    target_player = None
    for player in roster_list:
        if player.get("player_id") == player_id:
            target_player = player
            break
            
    if not target_player:
        print(f"\nKhông tìm thấy tuyển thủ mang mã {player_id}.")
        logging.warning(f"Failed to update player - Player ID {player_id} not found")
        return

    print(f"\nTuyển thủ: {target_player['name']}")
    print(f"Vị trí: {target_player['role']}")
    print(f"Lương hiện tại: {target_player['salary']:,}")
    print(f"Trạng thái hiện tại: {target_player['status']}")
    
    print("\nBạn muốn cập nhật:\n1. Cập nhật lương\n2. Cập nhật trạng thái thi đấu")
    
    while True:
        try:
            choice = input("Chọn chức năng cập nhật (1-2): ").strip()
            if choice == "1":
                while True:
                    try:
                        new_salary = float(input("Nhập mức lương mới: ").strip())
                        if new_salary <= 0:
                            print("Lương phải là số dương. Vui lòng nhập lại.")
                            continue
                        old_salary = target_player["salary"]
                        target_player["salary"] = new_salary
                        print(f"\nThành công: Đã cập nhật lương cho tuyển thủ {player_id}.")
                        logging.info(f"Updated player {player_id} salary from {old_salary} to {new_salary}")
                        return
                    except ValueError:
                        print("Mức lương phải là một con số số hợp lệ!")
            elif choice == "2":
                print("\nChọn trạng thái mới:\n1. Active\n2. Benched")
                while True:
                    status_choice = input("Nhập lựa chọn trạng thái (1-2): ").strip()
                    if status_choice == "1":
                        target_player["status"] = "Active"
                        break
                    elif status_choice == "2":
                        target_player["status"] = "Benched"
                        break
                    print("Lựa chọn không hợp lệ, vui lòng chỉ chọn 1 hoặc 2.")
                print(f"\nThành công: Đã cập nhật trạng thái cho tuyển thủ {player_id}.")
                logging.info(f"Updated player {player_id} status to {target_player['status']}")
                return
            else:
                print("Lựa chọn chức năng không hợp lệ, vui lòng nhập lại.")
        except ValueError:
            print("Vui lòng nhập số ký tự hợp lệ.")


def generate_payroll_report(roster_list: list) -> None:
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return
        
    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Trạng thái':<10} | {'Lương gốc':<12} | Lương thực nhận")
    print("-" * 80)
    
    total_payroll = 0.0
    try:
        for player in roster_list:
            actual_pay = calculate_actual_pay(player)
            print(f"{player['player_id']:<8} | {player['name']:<15} | {player['status']:<10} | {player['salary']:<12,.1f} | {actual_pay:,.1f}")
            total_payroll += actual_pay
            
        print("-" * 80)
        print(f"Tổng quỹ lương hàng tháng: {total_payroll:,}")
        logging.info(f"Generated monthly payroll report. Total: {total_payroll}")
        
    except KeyError as error_key:
        print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
        print("-" * 80)
        print("Tổng quỹ lương hàng tháng: 0.0")
        logging.error(f"Missing key while generating payroll report: {error_key}")


def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====")
        print("1. Xem đội hình thi đấu hiện tại")
        print("2. Chiêu mộ tuyển thủ mới")
        print("3. Cập nhật lương & Trạng thái thi đấu")
        print("4. Báo cáo quỹ lương hàng tháng")
        print("5. Thoát hệ thống")
        print("==================================================")
        
        menu_choice = input("Chọn chức năng (1-5): ").strip()
        
        if menu_choice == "1":
            display_roster(roster_db)
        elif menu_choice == "2":
            sign_player(roster_db)
        elif menu_choice == "3":
            update_player_status(roster_db)
        elif menu_choice == "4":
            generate_payroll_report(roster_db)
        elif menu_choice == "5":
            print("\nHệ thống đóng an toàn. Tạm biệt Huấn luyện viên!")
            logging.info("Roster management system closed down smoothly.")
            break
        else:
            print("\nLựa chọn ngoài phạm vi, vui lòng chọn lại từ 1 đến 5!")
            logging.warning(f"Invalid menu choice selected: '{menu_choice}'")


if __name__ == "__main__":
    main()