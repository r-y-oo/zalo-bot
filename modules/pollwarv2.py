from zlapi.models import Message
from config import PREFIX, ADMIN
import time
import threading
import os

des = {
    'version': "1.0.0",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "test warr lỏ"
}

is_polling = False 

def stop_polling(client, message_object, thread_id, thread_type):
    global is_polling
    is_polling = False
    client.replyMessage(Message(text="Đã dừng tạo cuộc khảo sát."), message_object, thread_id, thread_type)

def handle_warpoll_command(message, message_object, thread_id, thread_type, author_id, client):
    global is_polling 

    if author_id not in ADMIN:
        noquyen = "Bạn không có quyền để thực hiện điều này!"
        client.replyMessage(Message(text=noquyen), message_object, thread_id, thread_type)
        return

    command_parts = message.split()
    
    if len(command_parts) < 2:
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh hợp lệ (vd: warpoll on hoặc warpoll off)."), message_object, thread_id, thread_type)
        return

    action = command_parts[1].lower()

    if action == "off":
        stop_polling(client, message_object, thread_id, thread_type)
        return

    if action != "on":
        client.replyMessage(Message(text="Vui lòng chỉ định lệnh 'on' hoặc 'off'."), message_object, thread_id, thread_type)
        return

    user_id = None

    if message_object.mentions:
        user_id = message_object.mentions[0]['uid']
    elif message_object.quote:
        user_id = str(message_object.quote.ownerId)
    else:
        client.replyMessage(Message(text="Vui lòng tag một người dùng!"), message_object, thread_id, thread_type)
        return
    try:
        author_info = client.fetchUserInfo(user_id)
        if isinstance(author_info, dict) and 'changed_profiles' in author_info:
            user_data = author_info['changed_profiles'].get(user_id, {})
            username = user_data.get('zaloName', 'không xác định')
        else:
            username = "Người dùng không xác định"
    except Exception as e:
        username = "Người dùng không xác định"
    try:
        file_path = os.path.join("modules", "cache", "name.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            captions = file.readlines()
            captions = [caption.strip() for caption in captions if caption.strip()]
    except FileNotFoundError:
        client.replyMessage(Message(text="Không tìm thấy file name.txt"), message_object, thread_id, thread_type)
        return
    if not captions:
        client.replyMessage(Message(text="File name.txt không có nội dung nào để gửi."), message_object, thread_id, thread_type)
        return
    is_polling = True

    def poll_loop():
        index = 0  
        while is_polling:
            question = f"{username} {captions[index]}"
            try:
                client.createPoll(question=question, options=["𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 Cha Mayy Ma?? ", "🐤"], groupId=thread_id)
                index = (index + 1) % len(captions)
                time.sleep(1)
            except Exception as e:
                client.replyMessage(Message(text=f"Lỗi khi tạo cuộc khảo sát: {str(e)}"), message_object, thread_id, thread_type)
                break

    poll_thread = threading.Thread(target=poll_loop)
    poll_thread.start()

def get_mitaizl():
    return {
        'chui40': handle_warpoll_command
    }