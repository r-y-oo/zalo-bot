import os
import requests
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.9.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "trò chuyện với Dthais"
}

def is_admin(author_id):
    return author_id == ADMIN

def read_command_content(command_name):
    """Đọc nội dung của lệnh từ tệp."""
    path = f"modules/{command_name}.py"
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Lỗi khi đọc file: {e}"
    return None

def create_mock_link(content):
    """Tạo link runmocky từ nội dung lệnh."""
    try:
        data = {
            "status": 200,
            "content": content,
            "content_type": "application/json",
            "charset": "UTF-8",
            "secret": "VIP",
            "expiration": "never"
        }
        response = requests.post("https://api.mocky.io/api/mock", json=data)
        response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
        mock_url = response.json().get("link")
        return mock_url if mock_url else "Không thể tạo link từ Mocky."
    except requests.exceptions.RequestException as e:
        return f"Lỗi HTTP: {str(e)}"
    except Exception as e:
        return f"Lỗi khi tạo mock link: {str(e)}"

def handle_share_command(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh share với quyền admin."""
    if not is_admin(author_id):
        client.replyMessage(Message(text="Bạn không có quyền sử dụng lệnh này."), message_object, thread_id, thread_type)
        return
    
    command_name = message.split()[1].strip() if len(message.split()) > 1 else None
    if not command_name:
        client.replyMessage(Message(text="Vui lòng nhập tên lệnh cần chia sẻ."), message_object, thread_id, thread_type)
        return

    content = read_command_content(command_name)
    
    if not content:
        client.replyMessage(Message(text=f"Lệnh '{command_name}' không tồn tại."), message_object, thread_id, thread_type)
        return
    
    mock_url = create_mock_link(content)
    response_message = f"Link runmocky: {mock_url}" if "http" in mock_url else mock_url
    client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)

def get_mitaizl():
    return {'chiase': handle_share_command}