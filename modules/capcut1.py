from zlapi import ZaloAPI
from zlapi.models import *
import os
import random
import json
import requests

des = {
    'version': "1.0.1",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Gửi video ngẫu nhiên từ danh sách JSON"
}

def handle_chill_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        with open('Api/capcut1.json', 'r', encoding='utf-8') as json_file:
            video_data = json.load(json_file)

        if video_data and isinstance(video_data, list):
            video_url = random.choice(video_data)
            thumbnail_url = "https://i.imgur.com/YonVsQX.mp4,https://i.imgur.com/28KglL1.mp4" 
            duration = 0
            width = 1920
            height = 1080
            # thông báo khi gửi video
            loading_message = Message(text="🔎đang tìm kiếm video capcut1 để gửi lên..vui lòng chờ trong giây lát🚦✨")
            client.sendMessage(loading_message, thread_id, thread_type, ttl=250000)
             # Thông điệp khi gửi video
            success_message = (
                "🎬 video capcut 1 của bạn đây! 🎶\n"
                "✨hãy cùng tận hưởng những niềm vui 🌟"
            )
            
            # Gửi video qua API
            client.sendRemoteVideo(
                videoUrl=video_url,
                thumbnailUrl='https://i.imgur.com/f3nK6z5.jpeg',
                duration=duration,
                thread_id=thread_id,
                thread_type=thread_type,
                width=width,
                height=height,
                message=Message(text=success_message)  
            )
            
            # Thông báo sau khi video đã được gửi
            found_message = "tải thành công video capcut1,ghi capcut2 để xem videoi tiếp theo✨"
            client.send(
                Message(text=found_message),
                thread_id=thread_id,
                thread_type=thread_type
            )
            
        else:
            client.send(
                Message(text="Danh sách video rỗng hoặc không hợp lệ."),
                thread_id=thread_id,
                thread_type=thread_type
            )
    except Exception as e:
        error_text = f"Lỗi xảy ra: {str(e)}"
        client.send(
            Message(text=error_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

def get_mitaizl():
    return {
        'capcut1': handle_chill_command
    }