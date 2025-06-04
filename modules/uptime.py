from zlapi.models import Message
import time
import os
import requests
import random

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Xem thời gian bot hoạt động"
}

start_time = time.time()

def handle_uptime_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)

        days = uptime_seconds // (24 * 3600)
        uptime_seconds %= (24 * 3600)
        hours = uptime_seconds // 3600
        uptime_seconds %= 3600
        minutes = uptime_seconds // 60
        seconds = uptime_seconds % 60

        uptime_message = f"Bot đã hoạt động được {days} ngày, {hours} giờ, {minutes} phút, {seconds} giây."
        message_to_send = Message(text=uptime_message)

        image_list_url = "https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listimg.json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        response = requests.get(image_list_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        
        if isinstance(json_data, dict) and 'url' in json_data:
            image_url = json_data.get('url')
        elif isinstance(json_data, list):
            image_url = random.choice(json_data)
        else:
            raise Exception("Dữ liệu trả về không hợp lệ")

        image_response = requests.get(image_url, headers=headers)
        image_path = 'modules/cache/temp_image5.jpeg'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        if os.path.exists(image_path):
            client.sendLocalImage(
                image_path, 
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type
            )
            os.remove(image_path)
        else:
            raise Exception("Không thể lưu ảnh")
    
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'uptime': handle_uptime_command
    }
