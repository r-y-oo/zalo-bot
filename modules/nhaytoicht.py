from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, Mention, MessageStyle
from config import ADMIN

is_onetag_running = False

des = {
    'version': "1.0.2",
    'credits': "Khang X Bot",
    'description': "Chửi chết cụ 1 con chó được tag"
}

def stop_onetag(client, message_object, thread_id, thread_type):
    global is_onetag_running
    is_onetag_running = False
    client.replyMessage(Message(text="WAR CON CẶC BỐ M TEST🐧."), message_object, thread_id, thread_type)

def handle_onetag_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_onetag_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="lũ óc cặc xin cha 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 chưa mà dùng vậy cn đĩ mẹ cn đĩ tâm thần👉🧠🫵"),

            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: onetag on hoặc onetag stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_onetag_running:
            client.replyMessage(
                Message(text="⚠️ **WAR CON CẶC BỐ M TEST🐧.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_onetag(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    if message_object.mentions:
        tagged_users = message_object.mentions[0]['uid']
    else:
        client.replyMessage(Message(text="Đợi Tí ! 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 Vui Lòng Chọn Người Muốn Tag"), message_object, thread_id, thread_type)
        return

    try:
        with open("nhay.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="Không tìm thấy file tag.txt."),
            message_object,
            thread_id,
            thread_type
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="File tag.txt không có nội dung nào để gửi."),
            message_object,
            thread_id,
            thread_type
        )
        return

    is_onetag_running = True
    def onetag_loop():
        while is_onetag_running:
            for noidung in Ngon:
                if not is_onetag_running:
                    break
                mention = Mention(tagged_users, length=0, offset=0)
                client.send(Message(text=f" {noidung}", mention=mention), thread_id, thread_type)
                time.sleep(0.00008)

    onetag_thread = threading.Thread(target=onetag_loop)
    onetag_thread.start()

def get_mitaizl():
    return {
        'chui43': handle_onetag_command
    }