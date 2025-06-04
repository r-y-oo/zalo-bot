import time
from zlapi.models import Message, ThreadType
from datetime import datetime, timedelta
import pytz
import threading
des = {"version": "1.0.2", "credits": "Hiển", "description": "welcomeImg"}

# Tin nhắn bot sẽ gửi mỗi 40 phút
message_to_send = " https://zalo.me/g/qpsdxz618 Bot Auto Rải Link"

# Timezone cho Việt Nam
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Define danh sách admin
ADMIN = ['8499074262308020780']  # Thay thế bằng ID của admin thực tế

def start_auto(client):
    all_group = client.fetchAllGroups()
    allowed_thread_ids = [gid for gid in all_group.gridVerMap.keys() if gid != '9034032228046851908']

    last_sent_time = None

    while True:
        now = datetime.now(vn_tz)
        
        # Gửi tin nhắn cứ mỗi 30 phút
        if last_sent_time is None or now - last_sent_time >= timedelta(minutes=60):
            for thread_id in allowed_thread_ids:
                gui = Message(text=message_to_send)
                try:
                    # Gửi tin nhắn vào nhóm
                    client.sendMessage(message=gui, thread_id=thread_id, thread_type=ThreadType.GROUP)
                    time.sleep(0.3)  # Thời gian chờ giữa các lần gửi tin nhắn
                except Exception as e:
                    print(f"Error sending message to {thread_id}: {e}")
            last_sent_time = now
        
        # Đợi 10 giây trước khi kiểm tra lại
        time.sleep(10)  # Chỉnh sửa từ 60s thành 10s

def handle_autosend_start(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra nếu người gửi là admin
    if author_id not in ADMIN:
        response_message = Message(text="🚫 **Bạn không có quyền để thực hiện điều này!**")
        client.replyMessage(response_message, message_object, thread_id, thread_type)
        return

    # Bắt đầu gửi tin nhắn tự động trong luồng riêng
    threading.Thread(target=start_auto, args=(client,), daemon=True).start()
    response_message = Message(text="Đã Bắt Đầu Chạy ✅🚀")
    client.replyMessage(response_message, message_object, thread_id, thread_type)

def get_mitaizl():
    return {
        'rao': handle_autosend_start
    }
    