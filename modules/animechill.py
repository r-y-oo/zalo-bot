from zlapi.models import Message
import requests

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 ",
    'description': "Gửi video anime chill"
}

def handle_vdgai_command(message, message_object, thread_id, thread_type, author_id, client):
    uptime_message = "☝️Video chill của 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 đây\n\n."
    message_to_send = Message(text=uptime_message)
    
    url = 'https://api-dowig.onrender.com/images/videochill'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        video_url = data.get('url', '')  # Lấy URL của video từ API
        duration = '100'  # Đặt độ dài của video (giả định)

        # Gửi video mà không có thumbnail (ảnh nền)
        client.sendRemoteVideo(
            video_url, 
            None,  # Không truyền thumbnail để loại bỏ ảnh nền
            duration=duration,
            message=message_to_send,  # Gửi tin nhắn kèm video
            thread_id=thread_id,
            thread_type=thread_type,
            ttl=120000,  # Thời gian tồn tại tin nhắn
            width=1080,
            height=1920
        )
        
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)

def get_mitaizl():
    return {
        'animechill': handle_vdgai_command  # Đảm bảo đây là key 'animechill' để liên kết lệnh
    }