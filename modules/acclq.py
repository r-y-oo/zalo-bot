import random
import time
from zlapi.models import Message

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "Áp dụng code all link raw"
}

# Đọc danh sách tài khoản từ file
def read_accounts_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            accounts = file.readlines()
        return [account.strip() for account in accounts]
    except Exception as e:
        print(f"Lỗi khi đọc file: {str(e)}")
        return []

# Hàm xử lý lệnh gửi tài khoản game
def handle_send_accounts_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        # Lấy số lượng tài khoản yêu cầu từ tin nhắn
        try:
            num_accounts = int(message.split()[1])
        except (IndexError, ValueError):
            client.replyMessage(Message(text="Vui lòng cung cấp số lượng tài khoản hợp lệ sau lệnh."), message_object, thread_id, thread_type,ttl=20000)
            return

        # Đọc tài khoản từ file
        accounts = read_accounts_from_file('lq.txt')
        if not accounts:
            client.replyMessage(Message(text="Không thể đọc danh sách tài khoản."), message_object, thread_id, thread_type,ttl=10000)
            return

        # Kiểm tra nếu số lượng yêu cầu vượt quá số lượng tài khoản có sẵn
        if num_accounts > len(accounts):
            client.replyMessage(Message(text=f"Chỉ có {len(accounts)} tài khoản có sẵn."), message_object, thread_id, thread_type,ttl=120000)
            return

        # Chọn ngẫu nhiên số lượng tài khoản được yêu cầu
        selected_accounts = random.sample(accounts, num_accounts)

        # Tạo tin nhắn chứa danh sách tài khoản
        message_to_send = "Danh sách tài khoản game liên quân của bạn:\n" + "\n".join(selected_accounts)

        # Gửi tin nhắn
        client.replyMessage(Message(text=message_to_send), message_object, thread_id, thread_type,ttl=120000)
        print(f"Đã gửi {num_accounts} tài khoản cho người dùng {author_id}")

    except Exception as e:
        error_message = f"Lỗi khi gửi tài khoản: {str(e)}"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type,ttl=120000)

# Đăng ký lệnh với bot
def get_mitaizl():
    return {
        'acclq': handle_send_accounts_command
    }