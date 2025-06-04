from zlapi.models import Message
import json
import urllib.parse
import os
import requests
import urllib.parse
import io
from PIL import Image, ImageDraw
from removebg import RemoveBg

des = {
    'version': "1.0.0",
    'credits': "Duy Khannh",
    'description': "Tạo sticker (tách nền) khi reply vào một ảnh"
}

class BackgroundRemover:
    def __init__(self, api_key):
        self.rmbg = RemoveBg(api_key, "error.log")

    def remove_background_from_url(self, img_url):
        try:
            output_file_name = 'no-bg.png'
            self.rmbg.remove_background_from_img_url(img_url, new_file_name=output_file_name)
            return output_file_name
        except Exception as e:
            print(f"Lỗi khi xóa nền từ URL: {e}")
            return None

def handle_stk_command(message, message_object, thread_id, thread_type, author_id, client):
    if message_object.quote:
        attach = message_object.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
            except json.JSONDecodeError:
                client.sendMessage(
                    Message(text="Dữ liệu ảnh không hợp lệ."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            image_url = attach_data.get('hdUrl') or attach_data.get('href')
            if not image_url:
                client.sendMessage(
                    Message(text="Không tìm thấy URL ảnh."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return
            image_url = image_url.replace("\\/", "/")
            image_url = urllib.parse.unquote(image_url)
            if is_valid_image_url(image_url):
                remover = BackgroundRemover("MP3C65G5u1y9HyUPiZmjVbEW") #deo xoa dong nay 
                output_file_name = remover.remove_background_from_url(image_url)
                if output_file_name:
                    webp_image_url = convert_image_to_webp(output_file_name)
                    if webp_image_url:
                        try:
                            client.sendCustomSticker(
                                staticImgUrl=image_url,
                                animationImgUrl=webp_image_url,
                                thread_id=thread_id,
                                thread_type=thread_type
                            )
                            client.sendMessage(
                                Message(text="Sticker đã được tạo!"), 
                                thread_id=thread_id, 
                                thread_type=thread_type
                            )
                        except Exception as e:
                            client.sendMessage(
                                Message(text=f"Không thể gửi sticker: {str(e)}"),
                                thread_id=thread_id, 
                                thread_type=thread_type
                            )
                    else:
                        client.sendMessage(
                            Message(text="Không thể chuyển đổi hình ảnh."),
                            thread_id=thread_id, 
                            thread_type=thread_type
                        )
                else:
                    client.sendMessage(
                        Message(text="Không thể xóa nền."),
                        thread_id=thread_id, 
                        thread_type=thread_type
                    )
            else:
                client.sendMessage(
                    Message(text="URL không phải là ảnh hợp lệ."),
                    thread_id=thread_id, 
                    thread_type=thread_type
                )
        else:
            client.sendMessage(
                Message(text="Không có ảnh nào được reply."),
                thread_id=thread_id, 
                thread_type=thread_type
            )
    else:
        client.sendMessage(
            Message(text="Hãy reply vào ảnh cần tạo sticker."),
            thread_id=thread_id, 
            thread_type=thread_type
        )

def is_valid_image_url(url):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def convert_image_to_webp(image_path):
    try:
        with Image.open(image_path) as image:
            buffered = io.BytesIO()
            image.save(buffered, format="WEBP")
            buffered.seek(0)
            webp_image_url = upload_to_catbox(buffered)
            return webp_image_url
    except Exception as e:
        print("Lỗi trong quá trình chuyển đổi:", e)
    return None

def upload_to_catbox(buffered):
    url = "https://catbox.moe/user/api.php"
    files = {
        'fileToUpload': ('image.webp', buffered, 'image/webp')
    }
    data = {
        'reqtype': 'fileupload'
    }
    response = requests.post(url, files=files, data=data)
    print("Nội dung phản hồi từ Catbox:", response.text)
    if response.status_code == 200:
        if response.text.startswith("http"):
            return response.text
        else:
            print("Lỗi khi upload:", response.text)
    else:
        print("Lỗi kết nối:", response.status_code)
    return None

def get_mitaizl():
    return {
        'taostk': handle_stk_command
    }