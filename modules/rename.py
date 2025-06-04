import threading
from zlapi.models import Message
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import random

# Danh sách emoji để thả reaction
EMOJI_LIST = ["😍", "🥀", "👻", "💤", "😂", "🔥", "💖", "🤡", "🦋", "✨"]

# Đường dẫn font chữ (thay thế bằng font có sẵn trên hệ thống)
FONT_PATH = "font/2.ttf"

# Hàm gửi 6 icon ngẫu nhiên trước khi gửi tin nhắn rename
def send_random_reactions(client, message_object, thread_id, thread_type):
    chosen_emojis = random.sample(EMOJI_LIST, 6)  # Chọn 6 icon ngẫu nhiên
    for emoji in chosen_emojis:
        try:
            client.sendReaction(message_object, emoji, thread_id, thread_type, reactionType=75)
        except Exception as e:
            print(f"Lỗi khi gửi reaction {emoji}: {e}")

# Hàm tạo ảnh với nền galaxy tối đậm hơn và chấm sao rõ nét hơn
def create_galaxy_image(new_name):
    width, height = 1200, 600  # Full size ảnh lớn hơn

    # Tạo nền galaxy tối hơn (gần như đen)
    bg_image = Image.new("RGB", (width, height), (10, 10, 30))  # Màu gần đen
    draw = ImageDraw.Draw(bg_image)

    for x in range(width):
        for y in range(height):
            r = int(10 + 40 * (x / width) + 20 * (y / height))  # Màu tối hơn
            g = int(5 + 60 * (y / height))
            b = int(20 + 80 * (x / width))
            draw.point((x, y), fill=(r, g, b))

    # Thêm chấm sao sáng hơn, rõ nét
    for _ in range(350):  # Tăng số lượng sao
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        star_size = random.randint(3, 6)  # Ngôi sao to hơn
        draw.ellipse((x, y, x + star_size, y + star_size), fill="white")  # Chấm sao đậm màu trắng

    # Vẽ chữ
    font = ImageFont.truetype(FONT_PATH, 60)
    text = " Đổi Tên Thành Công!"
    text2 = f" Tên Mới: {new_name}"

    # Tính toán vị trí chữ cho cân đối
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (width - text_width) // 2
    text_y = height // 3

    text2_width, text2_height = draw.textbbox((0, 0), text2, font=font)[2:]
    text2_x = (width - text2_width) // 2
    text2_y = text_y + 80

    draw.text((text_x, text_y), text, font=font, fill="white")
    draw.text((text2_x, text2_y), text2, font=font, fill="white")

    # Lưu ảnh
    image_path = "rename_success.jpg"
    bg_image.save(image_path)
    return image_path

# Hàm xử lý lệnh rename
def handle_rename_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = "🚦 Sai cú pháp (ví dụ: dt trungchill Cte)"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)
        return

    new_name = " ".join(content[1:])

    # ID người dùng được cấp quyền
    authorized_id = "8499074262308020780"  # Thay bằng ID admin

    if author_id != authorized_id:
        error_message = "🚦 Bạn Không Có Quyền Sử Dụng Lệnh Này"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)
        return

    # Thả 6 icon random trước khi gửi tin nhắn rename
    send_random_reactions(client, message_object, thread_id, thread_type)

    # Gửi tin nhắn "Đang rename..."
    waiting_message = "🔄 Đang đổi tên tài khoản của bạn, vui lòng chờ...☘️"
    client.replyMessage(Message(text=waiting_message), message_object, thread_id, thread_type)

    def change_name_task():
        try:
            user = client.fetchAccountInfo().profile
            biz = user.bizPkg.label if user.bizPkg.label else {}
            dob = '2000-04-26'  # Ngày sinh mặc định
            gender = int(user.gender) if user.gender else 0  # 0: Nam, 1: Nữ

            client.changeAccountSetting(name=new_name, dob=dob, gender=gender, biz=biz)

            # Tạo ảnh xác nhận đổi tên
            image_path = create_galaxy_image(new_name)

            # Gửi ảnh xác nhận, đảm bảo hiển thị full không cần bấm vào
            client.sendLocalImage(image_path, thread_id, thread_type, width=1200, height=600)

            # Gửi tin nhắn thông báo rename thành công
            success_message = f"✨ Đã đổi tên tài khoản thành công!\n🎉 Tên mới: {new_name}"
            client.replyMessage(Message(text=success_message), message_object, thread_id, thread_type)

            # Xóa file sau khi gửi
            os.remove(image_path)

        except Exception as e:
            error_message = f"🚦 Lỗi khi đổi tên tài khoản: {e}"
            client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)

    threading.Thread(target=change_name_task).start()

# Đăng ký lệnh vào module
def get_mitaizl():
    return {
        'dt': handle_rename_command
    }