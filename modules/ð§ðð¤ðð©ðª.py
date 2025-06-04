from zlapi.models import Message
import requests
des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "𝔾𝕦̛̉𝕚 𝕧𝕚𝕕𝕖𝕠 𝕤𝕖𝕩𝕪"
}

def handle_vdsexy_command(message, message_object, thread_id, thread_type, author_id, client):
    uptime_message = "Video gái của 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 đây."
    message_to_send = Message(text=uptime_message)
    
    api_url = 'https://vdang1.sbs/videos/vdsexy'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        video_url = data.get('url', '')
        thumbnail_url = 'https://vdang1.sbs/images/gaisexy'
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
        'vdsexy': handle_vdsexy_command
    }
