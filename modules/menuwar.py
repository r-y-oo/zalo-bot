from zlapi import ZaloAPI
from zlapi.models import *
import time
import importlib
import threading
import requests
from io import BytesIO
import pytz
import random
import os
from PIL import ImageChops
import emoji
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from zlapi.models import Message
from config import PREFIX

# HÀM TẢI AVATAR 
def download_avatar(avatar_url, save_path="modules/cache/user_avatar.png"):
    try:
        if not os.path.exists("modules/cache"):
            os.makedirs("modules/cache", exist_ok=True)
        resp = requests.get(avatar_url, stream=True, timeout=10)
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            return save_path
        else:
            print(f"Không thể tải ảnh từ {avatar_url}, mã trạng thái: {resp.status_code}")
            return None
    except Exception as e:
        print(f"Lỗi download_avatar: {e}")
        return None

def process_avatar(avatar_path, bg_image, box_x1, box_y1, box_x2, box_y2):
    if avatar_path:
        try:
            avatar = Image.open(avatar_path).convert("RGBA")
            avatar = avatar.resize((150, 150))  # Kích thước avatar
            mask = Image.new("L", avatar.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
            avatar.putalpha(mask)  # Apply the circular mask

            # Định vị avatar ở góc trái trong hộp
            avatar_x = box_x1 + 20  # Dịch avatar vào trong hộp
            avatar_y = (box_y1 + box_y2) // 2 - avatar.height // 2  # Căn giữa theo chiều dọc

            bg_image.paste(avatar, (avatar_x, avatar_y), avatar)  # Dán avatar lên nền
        except Exception as e:
            print(f"Lỗi xử lý avatar: {e}")


def get_user_name_by_id(bot, author_id):
    try:
        user_info = bot.fetchUserInfo(author_id).changed_profiles[author_id]
        return user_info.zaloName or user_info.displayName
    except Exception:
        return "Unknown User"

# MENU+FONT
def menuzl(message, message_object, thread_id, thread_type, author_id, client):
    user_name = get_user_name_by_id(client, author_id)
    image_dir = "background"
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("Không tìm thấy ảnh trong thư mục background!")
        return

    random_image = random.choice(image_files)
    image_path = os.path.join(image_dir, random_image)
    output_image_path = "output.png"
    
    # Kích thước 
    size = (1124, 402)
    # Màu hộp bo tròn: đen với độ trong suốt 180
    box_color = (0, 0, 0, 180)
    
    bg_image = Image.open(image_path).convert("RGBA").resize(size).filter(ImageFilter.GaussianBlur(8))
    overlay = Image.new("RGBA", size, (0))
    draw = ImageDraw.Draw(overlay)
    
    box_x1, box_y1 = 50, 30
    box_x2, box_y2 = size[0] - 50, size[1] - 30
    draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=35, fill=box_color)
    
    font_path = "font/arial.ttf"
    font_text = ImageFont.truetype(font_path, 42) if os.path.exists(font_path) else ImageFont.load_default()
    font_time = ImageFont.truetype(font_path, 38) if os.path.exists(font_path) else ImageFont.load_default()
    font_emoji_path = "font/emoji.ttf"
    font_icon = ImageFont.truetype(font_emoji_path, 150) if os.path.exists(font_emoji_path) else ImageFont.load_default()

    # Lấy thời gian Việt Nam (UTC+7)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vn_tz)
    time_text = current_time.strftime("%H:%M")
    time_emoji = "⏰"

    # Load font chữ thường
    font_path = "font/arial.ttf"
    font_time = ImageFont.truetype(font_path, 38) if os.path.exists(font_path) else ImageFont.load_default()

    # Load font emoji
    font_emoji_path = "font/emoji.ttf"
    font_emoji = ImageFont.truetype(font_emoji_path, 38) if os.path.exists(font_emoji_path) else font_time

    # Tính kích thước emoji và text
    emoji_size = draw.textbbox((0, 0), time_emoji, font=font_emoji)
    emoji_width = emoji_size[2] - emoji_size[0]

    text_size = draw.textbbox((0, 0), time_text, font=font_time)
    text_width = text_size[2] - text_size[0]

    # Tổng chiều rộng để căn phải trong hộp
    total_width = emoji_width + 8 + text_width  # 8px khoảng cách giữa emoji và chữ
    time_x = box_x2 - total_width - 40  # Cách lề phải 40px
    time_y = box_y1 + 20  # Cách trên 20px

    # Vẽ emoji và text tách biệt nhưng liền nhau
    draw.text((time_x, time_y), time_emoji, font=font_emoji, fill=(255, 255, 255))
    draw.text((time_x + emoji_width + 8, time_y), time_text, font=font_time, fill=(255, 255, 255))

    # Lấy avatar từ người dùng
    try:
        user = client.fetchUserInfo(author_id).changed_profiles[author_id]
        avatar_url = user.avatar
        avatar_path = download_avatar(avatar_url) if avatar_url else None
    except Exception as e:
        print(f"❌ Lỗi lấy thông tin user: {e}")
        avatar_path = None

    # Tạo layer mới cho avatar để đặt trên hộp
    avatar_layer = Image.new("RGBA", size, (0, 0, 0, 0))

    # Kiểm tra avatar và xử lý nếu có
    if avatar_path:
        try:
            avatar = Image.open(avatar_path).convert("RGBA")
            avatar = avatar.resize((150, 150))  # Kích thước avatar
            mask = Image.new("L", avatar.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
            avatar.putalpha(mask)  # Apply the circular mask

            # Định vị avatar ở góc trái trong hộp
            avatar_x = box_x1 + 20  # Dịch avatar vào trong hộp
            avatar_y = (box_y1 + box_y2) // 2 - avatar.height // 2  # Căn giữa theo chiều dọc

            avatar_layer.paste(avatar, (avatar_x, avatar_y), avatar)  # Dán avatar lên layer riêng
        except Exception as e:
            print(f"Lỗi xử lý avatar: {e}")
    
    text_lines = [
       f"Hi, {user_name}",
       f"Chào Mừng Đến Với Menu",
        "                                                         ",
       f"Bot Luôn Sẵn Sàng Phục Vụ Bạn",
       f"Bot: Duy Khanh | Version 0.0.1 | Update 10/5/2025"
    ]

    # Tạo một mask màu trắng cho các dòng chữ
    text_mask = Image.new("L", size, 0)
    mask_draw = ImageDraw.Draw(text_mask)

    for i, line in enumerate(text_lines):
        text_x = (box_x1 + box_x2) // 2 - len(line) * 10
        text_y = box_y1 + 70 + i * 50
        mask_draw.text((text_x, text_y), line, font=font_text, fill=255)

    overlay_alpha = overlay.split()[-1]
    new_alpha = ImageChops.subtract(overlay_alpha, text_mask)
    overlay.putalpha(new_alpha)
    
    random_icons = ["📋"]
    draw.text((box_x2 - 180, (box_y1 + box_y2) // 2 - 90), random.choice(random_icons), font=font_icon, fill=(248, 217, 224))
    
    # Chuẩn bị văn bản trong text
    text = f"""🚦@member
 • Menu Bot × Update
➜🔥[Toxic]: Thả Toxic
➜🌟[Spgr]: Lệnh Auto 
➜👽[War]: Lệnh War
➜💨[5C]: War 5 chữ
➜⚡[Nhạc]: Chọn Nhạc
➜🌊[Tag5c]: War Tag 5C
➜💵[Reo]: War Tag
➜🧭[chuinamebox]: war tên box
➜🌐[bucu]: war poll
➜💻[nhay]: war nhây
"""
    
    # Ghép các layer: nền -> overlay (hộp) -> avatar
    combined = Image.alpha_composite(bg_image, overlay)
    combined = Image.alpha_composite(combined, avatar_layer)
    combined.save(output_image_path, format="PNG")
    
    action = "👾"
    client.sendReaction(message_object, action, thread_id, thread_type, reactionType=75)
    client.sendLocalImage(
        imagePath=output_image_path,
        message=Message(text=text, mention=Mention(author_id, offset=len("🚦 "), length=len("@member"))),
        thread_id=thread_id,
        thread_type=thread_type,
        width=1124,
        height=402,
        ttl=60000
    )

# HÀM ĐĂNG KÝ LỆNH
def get_mitaizl():
    return {
        'menuwar': menuzl
    }