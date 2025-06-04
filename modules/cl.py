from zlapi import ZaloAPI
from zlapi.models import *
import time
from config import ADMIN
ADMIN_ID = ADMIN
from concurrent.futures import ThreadPoolExecutor
import threading
import requests

# hay tên trong tác giả không để xóa dòng này.
# xin cảm ơn

des = {
    "version": "1.0.0",
    "credits": "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    "description": "gửi video sex siêu mlem"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def handle_videosex_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        msg = "• Bạn không có quyền! Chỉ có admin mới có thể sử dụng được lệnh này."
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#f38ba8", auto_format=False),
            MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="11", auto_format=False)
        ])
        client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type, ttl=5000)
        return

    if hasattr(message_object, 'content') and isinstance(message_object.content, str):
        response = requests.get("https://api-dowig.onrender.com/images/videogaixinh")
        data = response.json()

        video_url = data.get("url")
        thumbnail_url = "https://i.imgur.com/vxZS3r6.jpeg"
        duration = 15000

        if video_url:
            text_response = requests.get("https://api-dowig.onrender.com/poem/cadao")
            if text_response.status_code == 200:
                text_data = text_response.json()
                content = text_data.get("data", "")
                width = 1080
                height = 1920

                client.sendRemoteVideo(
                    videoUrl=video_url,
                    thumbnailUrl=thumbnail_url,
                    duration=duration,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    message=Message(text=content),
                    width=width,
                    height=height,
                    ttl=5000000
                )
            else:
                client.send(Message(text="Lỗi khi gọi API lấy nội dung."), thread_id=thread_id, thread_type=thread_type)
        else:
            client.send(Message(text="Lỗi khi lấy video."), thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'clon': handle_videosex_command
    }