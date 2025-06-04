from zlapi.models import Message
import requests
des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "𝔾𝕦̛̉𝕚 𝕧𝕚𝕕𝕖𝕠 𝟙𝟠+"
}

def handle_vd18_command(message, message_object, thread_id, thread_type, author_id, client):
    uptime_message = "Video vd18 của bạn đây."
    message_to_send = Message(text=uptime_message)
    
    api_url = 'https://api.sumiproject.net/video/videosex?apikey=HUNGDEV_WcMqCOEcY0'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        video_url = data.get('url', '')
        thumbnail_url = 'https://files.catbox.moe/gjg8fg.jpeg'
        duration = '1000'

        client.sendRemoteVideo(
            video_url, 
            thumbnail_url,
            duration=duration,
            message=None,
            thread_id=thread_id,
            thread_type=thread_type,ttl=120000,
            width=1080,
            height=1920
        )
        
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type,ttl=120000)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type,ttl=120000)

def get_mitaizl():
    return {
        'vd18': handle_vd18_command
    }