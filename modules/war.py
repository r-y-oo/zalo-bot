from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, MessageStyle
from config import ADMIN

is_war_running = False

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Gửi nội dung từ file chui.txt liên tục trong nhóm."
}

def stop_war(client, message_object, thread_id, thread_type):
    global is_war_running
    is_war_running = False
    # Đã xóa thông báo dừng gửi nội dung

def handle_war_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_war_running

    if author_id not in ADMIN:
        # Đã xóa thông báo về quyền hạn
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        # Đã xóa thông báo khi thiếu lệnh hợp lệ
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_war_running:
            # Đã xóa thông báo khi gửi nội dung đã dừng
            return
        else:
            stop_war(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        # Đã xóa thông báo khi lệnh không hợp lệ
        return

    try:
        with open("chui.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        # Đã xóa thông báo khi không tìm thấy file
        return

    if not Ngon:
        # Đã xóa thông báo khi file không có nội dung
        return

    is_war_running = True

    def war_loop():
        while is_war_running:
            for noidung in Ngon:
                if not is_war_running:
                    break
                client.send(Message(text=noidung), thread_id, thread_type)
                time.sleep(0.30)

    war_thread = threading.Thread(target=war_loop)
    war_thread.start()

def get_mitaizl():
    return {
        'war': handle_war_command
    }