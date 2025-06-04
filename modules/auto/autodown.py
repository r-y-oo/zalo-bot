import re
import requests
from zlapi.models import Message

des = {
    'version': "1.0.5",
    'credits': "Nguyễn Đức Tài",
    'description': "autodown"
}

regex = r"https?://(?:www\.|m\.)?tiktok\.com/@[\w.-]+/video/\d+|https?://m\.tiktok\.com/v/\d+|https?://vm\.tiktok\.com/[\w-]+"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'application/json'
}

def handle_autodown_command(message, message_object, thread_id, thread_type, author_id, client):
    match = re.search(regex, message)
    if not match:
        return

    linkvd = match.group(0)
    api_url = f'https://api.sumiproject.net/tiktok?video={linkvd}'

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print(data)

        video_url = data.get('data', {}).get('data', {}).get('play', '')
        thumbnail_url = 'https://files.catbox.moe/34xdgb.jpeg'
        duration = '1000'

        if video_url:
            client.sendRemoteVideo(
                video_url,
                thumbnail_url,
                duration=duration,
                message=None,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920
            )
        else:
            error_message = Message(text="Không thể lấy video từ liên kết TikTok.")
            client.sendMessage(error_message, thread_id, thread_type)
    
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'autodown': handle_autodown_command
    }
