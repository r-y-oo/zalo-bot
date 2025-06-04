from zlapi.models import Message
from config import ADMIN  # Sử dụng danh sách admin từ config.py
import time

des = {
    'version': "1.1.1",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Add and Kick member from group by ID <user_id> <number_of_times>, perform add and kick multiple times",
    'quyen su dung': "admin box, admin bot"
}

# Hàm kiểm tra xem người dùng có phải là admin không
def is_admin(author_id):
    return author_id in ADMIN

# Hàm kick người dùng khỏi nhóm
def handle_kick_user_command(user_id, thread_id, thread_type, author_id, client):
    try:
        if hasattr(client, 'kickUsersInGroup'):
            response = client.kickUsersInGroup(user_id, thread_id)
            send_message = f"Đã sút thành công người dùng có ID {user_id} ra khỏi nhóm."
        else:
            send_message = "Không thể thực hiện hành động sút người dùng."
    except Exception as e:
        send_message = f"Lỗi khi sút người dùng: {str(e)}"

    gui = Message(text=send_message)
    client.sendMessage(gui, thread_id, thread_type)

# Hàm thêm người dùng vào nhóm bằng ID
def handle_add_user_command(user_id, thread_id, thread_type, author_id, client):
    try:
        if hasattr(client, 'addUsersToGroup'):
            response = client.addUsersToGroup([user_id], thread_id)
            send_message = f"Đã thêm thành công người dùng có ID {user_id} vào nhóm."
        else:
            send_message = "Không thể thực hiện hành động thêm người dùng."
    except Exception as e:
        send_message = f"Lỗi khi thêm người dùng: {str(e)}"

    gui = Message(text=send_message)
    client.sendMessage(gui, thread_id, thread_type)

# Hàm thực hiện cả add và kick người dùng nhiều lần
def handle_add_kick_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):  # Kiểm tra quyền admin
        error_message = Message(text="Bạn không có quyền thực hiện lệnh này.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    text = message.split()

    if len(text) < 3 or not text[2].isdigit():
        error_message = Message(text="Vui lòng sử dụng cú pháp: .addkick <ID> <số lần>.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    user_id = text[1]  # Lấy ID người dùng
    count = int(text[2])  # Số lần thực hiện

    for i in range(count):
        # Thêm người dùng vào nhóm
        handle_add_user_command(user_id, thread_id, thread_type, author_id, client)
        time.sleep(0.5)  # Đợi 0.5 giây để tránh giới hạn API
        
        # Kick người dùng khỏi nhóm
        handle_kick_user_command(user_id, thread_id, thread_type, author_id, client)
        time.sleep(0.5)  # Đợi 0.5 giây để tránh giới hạn API

def get_mitaizl():
    return {
        'kick': handle_kick_user_command,
        'add': handle_add_user_command,
        'addkick': handle_add_kick_command
    }
#chỉ sài đc addkick còn kick ad