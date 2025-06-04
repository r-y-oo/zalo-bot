import os
import time
import threading
from zlapi.models import MultiMsgStyle, MessageStyle, Message
from config import ADMIN

is_war_running = False

des = {
    'version': "1.0.2",
    'credits': "Không Cần Ai Biết",
    'description': "Gửi nội dung từ file ngonwar2.txt liên tục trong nhóm với chữ cực lớn và hình ảnh."
}

def stop_war(client, message_object, thread_id, thread_type):
    global is_war_running
    is_war_running = False
    client.replyMessage(Message(text="⛔ **WAR CON CẶC BỐ M TEST🐧.**"), message_object, thread_id, thread_type)

def handle_war_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_war_running

    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="⚠️ Bạn không có quyền sử dụng lệnh này."),
            message_object, thread_id, thread_type
        )
        return

    command_parts = message.split()
    if len(command_parts) < 2:
        client.replyMessage(Message(text="❗ Vui lòng chỉ định lệnh hợp lệ (vd: treoanh on hoặc treoanh stop)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "stop":
        if not is_war_running:
            client.replyMessage(
                Message(text="⚠️ **Hiện tại không có nội dung nào đang gửi.**"),
                message_object, thread_id, thread_type
            )
        else:
            stop_war(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="❗ Vui lòng chỉ định lệnh 'on' hoặc 'stop'."), message_object, thread_id, thread_type)
        return

    try:
        with open("ngonwar2.txt", "r", encoding="utf-8") as file:
            Ngon = file.readlines()
    except FileNotFoundError:
        client.replyMessage(
            Message(text="❗ Không tìm thấy file **ngonwar2.txt**."),
            message_object,
            thread_id,
            thread_type
        )
        return

    if not Ngon:
        client.replyMessage(
            Message(text="❗ File **ngonwar2.txt** không có nội dung nào để gửi."),
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
                # Chuyển đổi nội dung thành chữ to và nổi bật
                spam_text = f"🔊🔊🔊 **{noidung.strip().upper()}** 🔊🔊🔊"
                client.send(Message(text=spam_text), thread_id, thread_type)

                # Gửi kèm hình ảnh
                try:
                    client.sendLocalImage(
                        "1.jpg",
                        thread_id=thread_id,
                        thread_type=thread_type,
                        message=Message(text="📢 **Hãy chú ý nội dung này!**"),
                        ttl=120000
                    )
                except FileNotFoundError:
                    client.replyMessage(
                        Message(text="❗ Không tìm thấy file ảnh **3.jpg**."),
                        thread_id,
                        thread_type
                    )
                except Exception as e:
                    client.replyMessage(
                        Message(text=f"⚠️ Lỗi khi gửi hình ảnh: {e}"),
                        thread_id,
                        thread_type
                    )

                time.sleep(3)  # Giãn cách thời gian gửi

    war_thread = threading.Thread(target=war_loop)
    war_thread.start()

def get_mitaizl():
    return {
        'treoanh': handle_war_command
    }