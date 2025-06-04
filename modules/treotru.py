from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, MessageStyle
from config import ADMIN

is_war_running = False

des = {
    'version': "1.0.2",
    'credits': "TrBao",
    'description': "Gửi nội dung từ file ngontreotru.txt liên tục trong nhóm."
}

def stop_war(client, message_object, thread_id, thread_type):
    global is_war_running
    is_war_running = False
    client.replyMessage(Message(text="Đã dừng gửi nội dung."), message_object, thread_id, thread_type)

def handle_war_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_war_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="Thằng Mặt Cặc Lồn Thâm Được Phép Xử Dụng À Em Con Đĩ Mẹ Mày Nun Nha Con Chó Ngu Phèn Phế Chết Con Đĩ Mẹ Nun Mà Đụ Mẹ Đòi Dài Bot Của Ca NhatMinh À Em Djt Mẹ Mày Ảo Tưởng Ít Thôi Cẩm Phán Bố Đi Rồi Đụ Mẹ Bố Cho M Về Bú Sữa Mẹ Nha Cchos Dốt🤪😎👊 ??."),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: tru on hoặc tru stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_war_running:
            client.replyMessage(
                Message(text="⚠️ **Bot : Thưa Cha NhatMinh Đã Tha Cho Con Ngu Ảo Trình🤞🤪.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_war(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    try:
        with open("ngontreotru.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="Không tìm thấy file ngontreotru.txt."),
            message_object,
            thread_id,
            thread_type
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="File ngontreotru.txt không có nội dung nào để gửi."),
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
                client.send(Message(text=noidung), thread_id, thread_type)
                time.sleep(0.3)

    war_thread = threading.Thread(target=war_loop)
    war_thread.start()

def get_mitaizl():
    return {
        'treo': handle_war_command
    }