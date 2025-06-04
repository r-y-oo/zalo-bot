from zlapi.models import *
import requests
import os
from PIL import Image
from io import BytesIO

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_image_dimensions(url):
    image_response = requests.get(url)
    image = Image.open(BytesIO(image_response.content))
    width, height = image.size  # Get width and height of the image
    return width, height

def handle_poli_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        content = message.strip().split()
        args = content[1:]
        prompt = " ".join(args)
        if not args:
            client.replyMessage(Message(text=f"🌷Chào mừng  @{author_id} đã đến với Menu Vẽ Ảnh 🎨\n\n🌠Lệnh của bạn:➜taoanh [nội dung]: 🎨Tạo ảnh theo yêu cầu bạn cung cấp !\n\n ➜ taoanh on/off: ✈️Bật/tắt tính năng Vẽ Ảnh 🖌️\n\n 🌠Ví dụ: taoanh con hổ 🐯✅\n\n🌟Hãy cho tôi biết bạn muốn gì nhé 🐰💬", mention=Mention(author_id, length=len("@Member"), offset=0)), message_object, thread_id, thread_type)
            return
        api_url = f"https://image.pollinations.ai/prompt/{prompt}"
        response = requests.get(api_url)
        response.raise_for_status()

        image_name = 'temp_image.jpeg'

        image_path = os.path.join(base_dir, 'cache', image_name)

        with open(image_path, 'wb') as f:
            f.write(response.content)

        width, height = get_image_dimensions(api_url)

        message_to_send = Message(text=f"🌸𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜🌸\nẢnh của bạn được tạo từ mô tả: {prompt}🐰💬")

        client.sendLocalImage(
            image_path, 
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=width,
            height=height
        )

        os.remove(image_path)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'taoanh': handle_poli_command
    }