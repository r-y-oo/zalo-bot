from zlapi.models import Message
from config import ADMIN
import time
import threading

des = {
    'version': "1.0.1",
    'credits': "Vũ Xuân Kiên",
    'description': "bot"
}

# Global variable to control the spam loop
stop_spam = False

def handle_sendmsg_command(message, message_object, thread_id, thread_type, author_id, client):
    global stop_spam
    stop_spam = False  # Reset stop signal at the start of the function

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="bạn chưa được duyệt để sài bot ! vui lòng liên hệ admin 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 để được duyệt sài bot 🤖"),
            message_object, thread_id, thread_type
        )
        return

    # Lấy thời gian delay từ nội dung tin nhắn (giả định người dùng sẽ gửi như 'spam 2' để delay 2 giây)
    parts = message.split()
    delay = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0.5  # Mặc định delay 1 giây nếu không có số được chỉ định

    try:
        with open("cndi.txt", "r", encoding="utf-8") as file:
            messages = file.readlines()

        # Start a new thread to allow stopping the loop
        def spam_messages():
            for i, msg in enumerate(messages):
                if stop_spam:
                    client.sendMessage(Message(text=""), thread_id, thread_type,ttl=ttl)
                    break
                
                client.sendMessage(Message(text=msg.strip()), thread_id, thread_type,ttl=15000)
                time.sleep(0.5)

        # Run the spamming in a separate thread
        spam_thread = threading.Thread(target=spam_messages)
        spam_thread.start()

    except Exception as e:
        print(f"Error: {e}")
        client.sendMessage(Message(text="Lỗi!"), thread_id, thread_type)

# Function to stop spamming
def handle_stop_command(message, message_object, thread_id, thread_type, author_id, client):
    global stop_spam
    stop_spam = True 
    client.sendMessage(Message(text="WAR CON CẶC BỐ M TEST🐧 ."), thread_id, thread_type,ttl=30000)

def get_mitaizl():
    return {
        'chui42': handle_sendmsg_command,
        'stop': handle_stop_command
    }