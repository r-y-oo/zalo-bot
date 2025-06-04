from zlapi.models import Message
import requests
import urllib.parse
import os

des = {
    'version': "1.9.2",
    'credits': "𝙣𝙜𝙪𝙮𝙚̂̃𝙣 𝙦𝙪𝙖𝙣𝙜 𝙫𝙪̃",
    'description': "Tạo ảnh từ text"
}

def handle_text2img_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2 or not text[1].strip():
        error_message = Message(text="Vui lòng nhập nội dung hợp lệ để chuyển đổi thành ảnh.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    content = "".join(text[1:])
    encoded_text = urllib.parse.quote(content, safe='')

    try:
        apianh = f'https://subhatde.id.vn/giangsinh?text={encoded_text}'
        response = requests.get(apianh)
        response.raise_for_status()

        data = response.json()
        links = data.get('data', [])

        if len(links) < 2:
            error_message = Message(text="API không trả về đủ ảnh.")
            client.sendMessage(error_message, thread_id, thread_type)
            return

        image_paths = []
        for idx, link in enumerate(links):
            if link:
                image_response = requests.get(link)
                image_path = f'modules/cache/temp_image_{idx}.jpeg'
                
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                
                image_paths.append(image_path)

        if image_paths:
            for image_path in image_paths:
                if os.path.exists(image_path):
                    client.sendLocalImage(
                        image_path, 
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type,
                        width=1600,
                        height=1600
                    )
                    os.remove(image_path)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except KeyError as e:
        error_message = Message(text=f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi không xác định: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'giangsinh': handle_text2img_command
    }
