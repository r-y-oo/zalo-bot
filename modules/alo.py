from zlapi.models import Message
import requests
import urllib.parse

des = {
    'version': "1.9.2",
    'credits': "Duy Khanh",
    'description': "trò chuyện với Duy Khanh"
}

def handle_sim_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2:
        error_message = Message(text="💻𝐗𝐢𝐧 𝐂𝐡à𝐨 𝐓ô𝐢 𝐋à 𝐑𝐨𝐛𝐨𝐭 𝐂ủ𝐚 Duy Khanh\n Chủ Nhân Duy Khanh đ𝖺𝗇𝗀 𝖻ậ𝗇 𝖼ầ𝗇 𝗍ô𝗂 𝗀𝗂ú𝗉 𝗀ì ?>< 🐰")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    content = " ".join(text[1:])
    encoded_text = urllib.parse.quote(content, safe='')

    try:
        sim_url = f'https://subhatde.id.vn/sim?type=ask&ask={encoded_text}'
        response = requests.get(sim_url)
        response.raise_for_status()

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
        'alo': handle_sim_command
    }