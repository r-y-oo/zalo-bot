from zlapi.models import Message
import json
import urllib.parse
import os
import requests
import time

des = {
    'version': "1.4.1",
    'credits': "Nguyễn Đức Tài x TRBAYK (NGSON)",
    'description': "Làm nét hình ảnh gửi dạng img và link"
}

last_sent_image_url = None

def handle_lamnet_command(message, message_object, thread_id, thread_type, author_id, client):
    global last_sent_image_url

    msg_obj = message_object

    if msg_obj.msgType == "chat.photo":
        img_url = msg_obj.content.href.replace("\\/", "/")
        img_url = urllib.parse.unquote(img_url)
        last_sent_image_url = img_url
        send_image_link(img_url, thread_id, thread_type, client)

    elif msg_obj.quote:
        attach = msg_obj.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
            except json.JSONDecodeError as e:
                print(f"Lỗi khi phân tích JSON: {str(e)}")
                return

            image_url = attach_data.get('hdUrl') or attach_data.get('href')
            if image_url:
                send_image_link(image_url, thread_id, thread_type, client)
            else:
                send_error_message(thread_id, thread_type, client)
        else:
            send_error_message(thread_id, thread_type, client)

    else:
        send_error_message(thread_id, thread_type, client)

def handle_4k_command(image_url, thread_id, thread_type, client):
    if image_url:
        api_url = f"https://api.sumiproject.net/lamnet?link={image_url}"

        client.send(Message(text="Đang xử lý ảnh... Vui lòng đợi."), thread_id=thread_id, thread_type=thread_type)

        for _ in range(3):
            try:
                response = requests.get(api_url)
                response.raise_for_status()

                data = response.json()
                anhnet = data.get('upscaled_image', '')
                
                if anhnet:
                    image_url = anhnet
                else:
                    break

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 500:
                    client.send(Message(text=f"Lỗi server:  {e}"), thread_id=thread_id, thread_type=thread_type)
                    send_error_message(thread_id, thread_type, client, "Lỗi từ máy chủ. Vui lòng thử lại sau.")
                    return
                else:
                    print(f"Lỗi khi gọi API: {str(e)}")
                    send_error_message(thread_id, thread_type, client, "Lỗi không xác định.")
                    return
            except requests.exceptions.RequestException as e:
                print(f"Lỗi kết nối: {str(e)}")
                send_error_message(thread_id, thread_type, client, "Lỗi kết nối đến máy chủ.")
                return
            
            time.sleep(1)

        if anhnet:
            send_image_with_link(anhnet, "file ảnh đã làm nét của bạn đây", thread_id, thread_type, client)
        else:
            send_error_message(thread_id, thread_type, client, "Không thể làm nét ảnh.")

def send_image_with_link(anhnet, fileName, thread_id, thread_type, client):
    if anhnet:
        client.sendRemoteFile(
            fileUrl=anhnet,
            thread_id=thread_id,
            thread_type=thread_type,
            fileName=fileName,
            fileSize=None,
            extension="JPEG"
        )
    else:
        send_error_message(thread_id, thread_type, client, "Không thể gửi file.")

def send_error_message(thread_id, thread_type, client, error_message="Vui lòng reply ảnh hoặc link ảnh cần làm nét."):
    client.send(Message(text=error_message), thread_id=thread_id, thread_type=thread_type)

def send_image_link(image_url, thread_id, thread_type, client):
    handle_4k_command(image_url, thread_id, thread_type, client)

def get_mitaizl():
    return {
        'lamnet': handle_lamnet_command
    }
