from zlapi.models import *
import time
import threading
from zlapi.models import MessageStyle
from config import ADMIN

is_spam_running = False

des = {
    'version': "1.0.4",
    'credits': "Trần Gia Bảo ",
    'description': "Chức năng spam nhiều icon trong một dòng."
}

def stop_spam(client, message_object, thread_id, thread_type):
    global is_spam_running
    is_spam_running = False
    client.replyMessage(Message(text="Đã dừng spam icon."), message_object, thread_id, thread_type)

def handle_spam_icon_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_spam_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Quyền lồn biên giới"),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 3:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: icon on <icon> <số lần>)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()
    icon = command_parts[2]
    try:
        count = int(command_parts[3])
    except (IndexError, ValueError):
        count = 10  # Default to 10 times if no count is specified

    if action == "stop":
        if not is_spam_running:
            client.replyMessage(
                Message(text="⚠️ **Spam icon đã dừng lại.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_spam(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    is_spam_running = True

    def spam_loop():
        for _ in range(count):
            if not is_spam_running:
                break
            client.send(Message(text=icon * 5), thread_id, thread_type, ttl=15000)
            time.sleep(0.50)  # Wait for 2 seconds between sends

    spam_thread = threading.Thread(target=spam_loop)
    spam_thread.start()

def get_mitaizl():
    return {
        'icon': handle_spam_icon_command
    }