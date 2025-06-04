from zlapi.models import *
import datetime
import pytz
import random
des = {
    'version': "1.0.4",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "chỉ có hi chào"
}

def hi(self, message, message_object, thread_id, thread_type, author_id):
    if message.lower() in ["hello", "hi", "hai", "chào", "xin chào", "chao", "hí", "híí", "hì", "hìì", "lô", "hii", "helo", "hê nhô"]:
        GREETINGS = [
            "Tốt Lành 🥳", "Vui Vẻ 😄", "Hạnh Phúc ❤", "Yêu Đời 😘", 
            "May Mắn 🍀", "Full Năng Lượng ⚡", "Tuyệt Vời 😁", 
            "Tỉnh Táo 🤓", "Đầy Sức Sống 😽", "Nhiệt Huyết 🔥"
        ]

        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.datetime.now(tz).strftime('%H%M')
        hours = int(current_time)

        if 301 <= hours <= 400:
            session = "Sáng Tinh Mơ"
        elif 401 <= hours <= 700:
            session = "Sáng Sớm"
        elif 701 <= hours <= 1000:
            session = "Sáng"
        elif 1001 <= hours <= 1200:
            session = "Trưa"
        elif 1201 <= hours <= 1700:
            session = "Chiều"
        elif 1701 <= hours <= 1800:
            session = "Chiều Tà"
        elif 1801 <= hours <= 2100:
            session = "Tối"
        elif 2101 <= hours or hours <= 300:
            session = "Đêm"
        else:
            session = "Lỗi"

        greeting_text = random.choice(GREETINGS)

        response_text = f"Xin chào @Member! Chúc Bạn Một Buổi {session} {greeting_text}"
        mention = Mention(author_id, length=len("@Member"), offset=len("Xin chào "))

        self.client.replyMessage(
            Message(
                text=response_text, mention=mention
            ),
            message_object,
            thread_id,
            thread_type, ttl=20000
        )
        return

def get_mitaizl():
    return {
        'hi': None
    }