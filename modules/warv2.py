from zlapi.models import Message
from config import ADMIN
import threading

des = {
    'version': "1.0.1",
    'credits': "𝕄𝕣ℚ",
    'description': "𝕎𝕒𝕣 ℕ𝕘𝕦̛𝕠̛̀𝕚 𝕂𝕙𝕒́𝕔"
}
# Biến để theo dõi trạng thái cuộc chiến
war_active = False
war_thread = None  # Để lưu trữ luồng gửi tin nhắn

# Đọc câu nói từ tệp modules/cache/ngonwar.txt
def load_war_phrases(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading phrases: {e}")
        return []

# Danh sách câu khiêu khích
war_phrases = load_war_phrases('modules/cache/ngonwar.txt')

def war_thread_function(thread_id, thread_type, client):
    global war_active
    for phrase in war_phrases:
        if not war_active:  # Kiểm tra nếu cuộc chiến đã dừng
            break
        client.sendMessage(Message(text=phrase), thread_id, thread_type)

def handle_war_command(message, message_object, thread_id, thread_type, author_id, client):
    global war_active, war_thread
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Xin lỗi, bạn không có quyền thực hiện hành động này."),
            message_object, thread_id, thread_type
        )
        return

    if war_active:
        client.sendMessage(Message(text="Cuộc chiến đã diễn ra. Vui lòng dừng cuộc chiến trước khi bắt đầu lại!"), thread_id, thread_type)
        return

    war_active = True
    war_thread = threading.Thread(target=war_thread_function, args=(thread_id, thread_type, client))
    war_thread.start()  # Bắt đầu luồng gửi tin nhắn

def handle_stop_command(message, message_object, thread_id, thread_type, author_id, client):
    global war_active, war_thread
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Xin lỗi, bạn không có quyền thực hiện hành động này."),
            message_object, thread_id, thread_type
        )
        return

    if not war_active:
        client.sendMessage(Message(text="Không có cuộc chiến nào đang diễn ra."), thread_id, thread_type)
        return

    war_active = False  # Đánh dấu cuộc chiến đã dừng
    stop_message = "🛑 Cuộc chiến đã dừng lại! 🛑"

    try:
        client.sendMessage(Message(text=stop_message), thread_id, thread_type)
        
        # Chờ cho luồng kết thúc nếu đang chạy
        if war_thread is not None:
            war_thread.join()
            war_thread = None  # Đặt lại luồng

    except Exception as e:
        print(f"Error while stopping war message: {e}")
        client.sendMessage(Message(text="Đã xảy ra lỗi khi dừng cuộc chiến."), thread_id, thread_type)

def get_mitaizl():
    return {
        'warv2': handle_war_command,
        'stop': handle_stop_command
    }