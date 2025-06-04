from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, Mention, MessageStyle
from config import ADMIN

is_reo_running = False

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Chửi chết cụ 1 con chó được tag"
}

def stop_reo(client, message_object, thread_id, thread_type):
    global is_reo_running
    is_reo_running = False
    client.replyMessage(Message(text="Đã dừng treo tên."), message_object, thread_id, thread_type,ttl=60000)

def handle_reo_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_reo_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Mày nghĩ m đủ tuổi?🖕"),
            message_object, thread_id, thread_type,ttl=60000
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: treo on hoặc treo stop)."), message_object, thread_id, thread_type,ttl=60000)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_reo_running:
            client.replyMessage(
                Message(text="⚠️ **treo tên đã dừng lại.**"),
                message_object, thread_id, thread_type,tll=60000
            )
        else:
            stop_reo(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type,ttl=60000)
        return

    if message_object.mentions:
        tagged_users = message_object.mentions[0]['uid']
    else:
        client.replyMessage(Message(text="Tag con chó cần ửa"), message_object, thread_id, thread_type)
        return

    try:
        with open("ngonwar2.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="Không tìm thấy file noidung.txt."),
            message_object,
            thread_id,
            thread_type,
            ttl=5000
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="File noidung.txt không có nội dung nào để gửi."),
            message_object,
            thread_id,
            thread_type,
            ttl=12000
        )
        return

    is_reo_running = True
    def reo_loop():
        while is_reo_running:
            for noidung in Ngon:
                if not is_reo_running:
                    break
                mention = Mention(tagged_users, length=0, offset=0)
                client.send(Message(text=f" {noidung}", mention=mention), thread_id, thread_type,ttl=6000)
                time.sleep(0.5)

    reo_thread = threading.Thread(target=reo_loop)
    reo_thread.start()

def get_mitaizl():
    return {
        'treotag': handle_reo_command
    }
