from zlapi import ZaloAPI
from zlapi.models import *
import random

des = {
    'version': "1.0.0",
    'Người Sử Dụng': "Thành Viên",
    'description': "Bói Tình Duyên"
}

# Hàm bói tình duyên với phần trăm ngẫu nhiên
def boi_tinh_duyen(ten_nam, ten_nu):
    return random.randint(0, 100)  # Tạo số ngẫu nhiên từ 0 đến 100

# Hàm xử lý lệnh bói tình duyên
def handle_boi_tinh_duyen_command(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra xem mentions có tồn tại hay không
    if not message_object.mentions or len(message_object.mentions) == 0:
        client.replyMessage(
            Message(text="Vui lòng tag đúng 2 người để bói tình duyên!"),
            message_object,
            thread_id,
            thread_type,
            ttl=10000
        )
        return
    elif len(message_object.mentions) < 2:
        client.replyMessage(
            Message(text="Bạn cần tag đủ 2 người để bói tình duyên!"),
            message_object,
            thread_id,
            thread_type,
            ttl=10000
        )
        return
    elif len(message_object.mentions) > 2:
        client.replyMessage(
            Message(text="Chỉ được tag tối đa 2 người để bói tình duyên!"),
            message_object,
            thread_id,
            thread_type,
            ttl=10000
        )
        return

    # Lấy thông tin hai người được tag
    uid1 = message_object.mentions[0].uid
    uid2 = message_object.mentions[1].uid
    name1 = client.fetchUserInfo(uid1).changed_profiles[uid1].displayName
    name2 = client.fetchUserInfo(uid2).changed_profiles[uid2].displayName

    # Tính độ hợp nhau ngẫu nhiên
    compatibility = boi_tinh_duyen(name1, name2)

    # Tạo cú pháp tag người dùng trong Zalo
    mention_text1 = f"@{name1}"
    mention_text2 = f"@{name2}"

    # Gửi kết quả với cú pháp tag người dùng
    client.replyMessage(
        Message(text=f"----------Độ hợp nhau của----------\n> {mention_text1} và {mention_text2} \n> Khoảng: {compatibility}%"),
        message_object,
        thread_id,
        thread_type,
        ttl=300000
    )

# Class kế thừa ZaloAPI
class Client(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
    
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        if not isinstance(message, str):
            return
        if author_id == self.uid:  # Không phản hồi tin nhắn của chính mình
            return
        
        if message.startswith("boi"):
            handle_boi_tinh_duyen_command(message, message_object, thread_id, thread_type, author_id, self)

# Hàm trả về các lệnh
def get_mitaizl():
    return {
        'tinhduyen': handle_boi_tinh_duyen_command
    }