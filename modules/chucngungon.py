from zlapi.models import Message
import requests
import urllib.parse

des = {
    'version': "1.9.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "trò chuyện với Qhuy"
}

def handle_sim_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2:
        error_message = Message(text="𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 𝗠𝘅𝗵 𝗧𝗿ù𝗺 𝗥é𝗼 𝗧ê𝗻 𝗩𝗻 Ô𝗻𝗴 𝗛𝗼à𝗻𝗴 𝗠𝗮𝗳𝗶𝗮 𝗜𝗻𝘁𝗲𝗿𝗻𝗲𝘁 𝗦ố 𝟭 𝗩𝗻 𝗫𝗶𝗻 𝗖𝗵ú𝗰 𝗕ạ𝗻 𝗡𝗴ủ 𝗡𝗴𝗼𝗮𝗻 𝗠ơ Đẹ𝗽 𝗡𝗵𝗼á ☄️ >~< 💖💤.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    content = " ".join(text[1:])
    encoded_text = urllib.parse.quote(content, safe='')

    try:
        cadao_url = f'https://i.imgur.com/RNONPnZ.jpg'
        {
  "dataGame": {
    "tukhoa": "phá rối",
    "sokitu": "☐☐☐ ☐☐☐",
    "suggestions": "P☐☐ R☐☐",
    "link": "https://i.imgur.com/RNONPnZ.jpg"
  }
}

        data = response.json()
        simi = data.get('answer', 'Không có phản hồi từ Simi.')
        message_to_send = Message(text=f"> Sim: {simi}")
        
        client.replyMessage(
            message_to_send,
            message_object,
            thread_id,
            thread_type
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
        'chucngungon': handle_sim_command
    }