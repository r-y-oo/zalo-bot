from zlapi.models import Message
import json
import urllib.parse
import os

des = {
    'version': "1.0.0",
    'credits': "Dzi x",
    'description': "Tạo sticker khi reply vào một ảnh"
}

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
                webp_image_url = convert_image_extension_to_webp(image_url)
                if "Định dạng ảnh không hợp lệ!" not in webp_image_url:
                    # Send custom sticker
                    client.send_custom_sticker(
                        animationImgUrl=webp_image_url,
                        staticImgUrl=webp_image_url,
                        thread_id=thread_id,
                        thread_type=thread_type,
                        reply=message_object,
                        width=None,
                        height=None
                    )
                    # Send separate confirmation message
                    client.sendMessage(
                        Message(text="Sticker đã được tạo!"), 
                        thread_id=thread_id, 
                        thread_type=thread_type
                    )
                else:
                    client.sendMessage(
                        Message(text="Hình ảnh không hợp lệ, không thể chuyển đổi."),
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
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', 'mp4']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def convert_image_extension_to_webp(image_url):
    file_name, file_extension = os.path.splitext(image_url)
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', 'mp4']
    
    if file_extension.lower() in valid_extensions:
        return file_name + '.webp'
    else:
        return "Định dạng ảnh không hợp lệ!"

def get_mitaizl():
    return {
        'taostk': handle_stk_command
    }