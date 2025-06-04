from zlapi.models import *
import os
import json
import requests
from PIL import Image
from io import BytesIO

# base_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(base_dir, 'cache', 'love.json')

def get_image_dimensions(url, headers):
    image_response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(image_response.content))
    width, height = image.size  # Get width and height of the image
    return width, height

def handle_4k_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        if message_object.quote:
            client.sendMessage(Message(text="Tiến hành xoá nền ảnh..."), thread_id, thread_type, ttl=5000)
            msgrep = message_object.quote
            attach_str = msgrep['attach']  # Lấy chuỗi JSON từ thuộc tính attach
            attach_data = json.loads(attach_str)  # Parse JSON thành đối tượng Python
            picture = attach_data['href']  # Lấy liên kết hình ảnh từ đối tượng đã parse
            converted_url = picture.replace("\\", "")  # Xóa các ký tự escape

            # url = "https://api.developer.pixelcut.ai/v1/upscale"

            # payload = json.dumps({
            #     "image_url": converted_url,
            #     "scale": 2
            # })
            # headers = {
            #     'Content-Type': 'application/json',
            #     'Accept': 'application/json',
            #     'X-API-KEY': 'sk_2a8fb05f3b464d948707504de06e1420'
            # }

            # response = requests.request("POST", url, headers=headers, data=payload)

            # print(response.text.result_url)
            api_url = f'https://www.hungdev.id.vn/ai/xoanen?url={converted_url}&apikey=gncEwY9xCc'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            image_url = data['data']

            image_response = requests.get(image_url, headers=headers)
            image_path = 'temp_image.jpg'

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            width, height = get_image_dimensions(image_url, headers)

            message_to_send = Message(text=f"Ảnh Đã Được Xoá Nền Thành Công")

            client.sendLocalImage(
                image_path,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=width,
                height=height
            )

            os.remove(image_path)

        else:
            client.replyMessage(Message(text="@Member, VUI LÒNG REPLY TIN NHẮN CẦN CHUYỂN THÀNH FULL HD !", mention=Mention(author_id, length=len("@Member"), offset=0)), message_object, thread_id, thread_type)
            return
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'xoanen': handle_4k_command
    }