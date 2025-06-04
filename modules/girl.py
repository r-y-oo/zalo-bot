import os
import random
import time
from zlapi.models import *
import requests

def handle_girl_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        # Image list URL
        image_list_url = "https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listimg.json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        # Fetch image list from the JSON file
        response = requests.get(image_list_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        
        # Select random image URL
        if isinstance(json_data, dict) and 'url' in json_data:
            image_url = json_data.get('url')
        elif isinstance(json_data, list):
            image_url = random.choice(json_data)
        else:
            raise Exception("Dữ liệu trả về không hợp lệ")

        # Download the image
        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()  # Ensure the image is downloaded successfully
        
        # Save the image temporarily
        temp_image_path = 'modules/cache/temp_image1.jpeg'
        with open(temp_image_path, 'wb') as f:
            f.write(image_response.content)

        # Send the image using sendLocalImage (pass image directly)
        if os.path.exists(temp_image_path):
            # Send the local image without specifying a keyword
            client.sendLocalImage(
                temp_image_path,  # Pass the path directly
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600
            )

            # After sending, remove the temporary image
            os.remove(temp_image_path)
        else:
            raise Exception("Không thể lưu ảnh")

    except requests.exceptions.RequestException as e:
        # Handle any exceptions during the request
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        # Handle other exceptions
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'girl': handle_girl_command
    }