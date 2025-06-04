from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, MessageStyle
from config import ADMIN

is_war_running = False

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Gửi nội dung từ file tho.txt liên tục trong nhóm."
}

def stop_war(client, message_object, thread_id, thread_type):
    global is_war_running
    is_war_running = False
    client.replyMessage(Message(text="Đã dừng gửi nội dung."), message_object, thread_id, thread_type)

def handle_war_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_war_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text=" Đĩ Mẹ Mày Con Chó Điên Mặt Cặc Cha 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 Cho Mày Sài Chưa?."),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: 1c on hoặc 1c stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_war_running:
            client.replyMessage(
                Message(text="⚠️ **Gửi nội dung đã dừng lại.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_war(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    try:
        with open("cuagai.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="Không tìm thấy file 1.txt."),
            message_object,
            thread_id,
            thread_type
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="File cuagai.txt không có nội dung nào để gửi."),
            message_object,
            thread_id,
            thread_type
        )
        return

    is_war_running = True

    def war_loop():
        while is_war_running:
            for noidung in Ngon:
                if not is_war_running:
                    break
                client.send(Message(text=noidung), thread_id, thread_type, ttl=120000)
                time.sleep(300)

    war_thread = threading.Thread(target=war_loop)
    war_thread.start()

def get_mitaizl():
    return {
        'tangai': handle_war_command
    }