from zlapi.models import Message
import requests

des = {
    'version': "1.0.2",
    'credits': "時崎狂三 ",
    'description': "Gửi video sẽ"
}

def handle_vdgai_command(message, message_object, thread_id, thread_type, author_id, client):
    uptime_message = "☝️Video sex của bạn đây\n\n."
    message_to_send = Message(text=uptime_message)
    
    url = 'https://api.sumiproject.net/video/videosex'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        video_url = data.get('url', '')
        thumbnail_url = 'https://files.catbox.moe/guyke9.jpg'
        duration = '100'

        client.sendRemoteVideo(
            video_url, 
            thumbnail_url,
            duration=duration,
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1080,
            height=1920
        )
        
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'sexv4': handle_vdgai_command
    }