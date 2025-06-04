from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Xem thời gian bot hoạt động"
}

# Hàm xử lý lệnh chặn người dùng theo UID
def handle_block_user_by_tag_or_uid(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra quyền admin
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Bạn không có quyền sử dụng lệnh này."),
            message_object, thread_id, thread_type
        )
        return

    # Phân tích cú pháp lệnh
    parts = message.split(' ', 2)
    if len(parts) < 2:
        response_message = (
            "Vui lòng cung cấp UID người dùng để chặn. "
            "Ví dụ: kb UID"
        )
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    # Lấy UID từ lệnh
    user_id = parts[1]
    if not user_id.isdigit():
        client.replyMessage(
            Message(text="UID không hợp lệ. Vui lòng nhập UID hợp lệ."),
            message_object, thread_id, thread_type
        )
        return

    try:
        # Chặn người dùng (API cần hỗ trợ lệnh này)
        client.blockUser(user_id)  # Gọi API Zalo để chặn người dùng
        success_message = f"Đã chặn người dùng với UID {user_id}. thằng này đã câm ko nhắn được nữa"
        client.replyMessage(Message(text=success_message), message_object, thread_id, thread_type)
    except Exception as e:
        error_message = f"Không thể chặn người dùng với UID {user_id}. Lỗi: {str(e)}"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)


# Hàm xử lý lệnh mở chặn người dùng theo UID
def handle_unblock_user_by_uid(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra quyền admin
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Bạn không có quyền sử dụng lệnh này."),
            message_object, thread_id, thread_type
        )
        return

    # Phân tích cú pháp lệnh
    parts = message.split(' ', 2)
    if len(parts) < 2:
        response_message = (
            "Vui lòng cung cấp UID người dùng để mở chặn. "
            "Ví dụ: unblock UID"
        )
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    # Lấy UID từ lệnh
    user_id = parts[1]
    if not user_id.isdigit():
        client.replyMessage(
            Message(text="UID không hợp lệ. Vui lòng nhập UID hợp lệ."),
            message_object, thread_id, thread_type
        )
        return

    try:
        # Mở chặn người dùng (API cần hỗ trợ lệnh này)
        client.unblockUser(user_id)  # Gọi API Zalo để mở chặn người dùng
        success_message = f"Đã mở chặn người dùng với UID {user_id}."
        client.replyMessage(Message(text=success_message), message_object, thread_id, thread_type)
    except Exception as e:
        error_message = f"Không thể mở chặn người dùng với UID {user_id}. Lỗi: {str(e)}"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)


# Hàm đăng ký các lệnh vào bot
def get_mitaizl():
    return {
        'block': handle_block_user_by_tag_or_uid,  # Lệnh chặn
        'unblock': handle_unblock_user_by_uid      # Lệnh mở chặn
    }