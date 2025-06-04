from zlapi import ZaloAPI
from zlapi.models import Message
import requests
import urllib.parse

des = {
    'version': "1.9.2",
    'credits': "Nguyễn Đức Tài",
    'description': "trò chuyện với simi"
}

def handle_joker_command(message, message_object, thread_id, thread_type, author_id, client):
    
    try:
        joker_url = f'https://www.hungdev.id.vn/others/phimRap?apikey=gncEwY9xCc'
        text_response = requests.get(joker_url)
                    
        if text_response.status_code == 200: 
            text_data = text_response.json()
            content = text_data.get("data", "Nội dung không có sẵn")
            message_to_send = Message(text=f"> : {content}")
            client.replyMessage(
                message_to_send,
                message_object,
                thread_id,
                thread_type,
                ttl=120000
            )

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
        'phimchieurap': handle_joker_command
    }