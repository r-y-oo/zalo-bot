import random
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi.models import Message, Mention
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import logging

des = {
    'version': "1.0.1",
    'credits': "trí",
    'description': "chào mấytk ngu"
}

logging.basicConfig(level=logging.ERROR, filename="bot_error.log", filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Hàm tạo ảnh nền đen
def create_black_background(width, height):
    return Image.new("RGB", (width, height), (0, 0, 0))

def create_gradient_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        colors.append((r, g, b))
    return colors

# Nội suy màu gradient
def interpolate_colors(colors, text_length, change_every, brightness_factor=1.2):
    gradient = []
    num_segments = len(colors) - 1
    steps_per_segment = (text_length // change_every) + 1

    for i in range(num_segments):
        for j in range(steps_per_segment):
            if len(gradient) < text_length:
                ratio = j / steps_per_segment
                interpolated_color = (
                    int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio),
                    int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio),
                    int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                )
                interpolated_color = tuple(min(int(c * brightness_factor), 255) for c in interpolated_color)
                gradient.append(interpolated_color)
    
    return gradient[:text_length]

# Tạo avatar hình tròn
def make_round_avatar(avatar):
    avatar_size = avatar.size
    avatar_mask = Image.new("L", avatar_size, 0)
    avatar_draw = ImageDraw.Draw(avatar_mask)
    avatar_draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)

    round_avatar = Image.new("RGBA", avatar_size, (255, 255, 255, 0))
    round_avatar.paste(avatar, (0, 0), avatar_mask)
    return round_avatar

# Điều chỉnh kích thước font sao cho phù hợp với chiều rộng
def adjust_font_size(draw, text, max_width, font_path, initial_size):
    font_size = initial_size
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    while text_width > max_width and font_size > 20:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textbbox((0, 0), text, font=font)[2]
    return font

# Vẽ chữ có viền
def draw_text_with_border(draw, text, position, font, gradient_colors, border_width=2):
    gradient = interpolate_colors(gradient_colors, text_length=len(text), change_every=4)
    x, y = position
    for i in range(len(text)):
        char = text[i]
        char_color = tuple(gradient[i])

        # Vẽ viền cho chữ
        for dx in range(-border_width, border_width + 1):
            for dy in range(-border_width, border_width + 1):
                if dx != 0 or dy != 0:  # Không vẽ viền ở vị trí chữ chính
                    draw.text((x + dx, y + dy), char, font=font, fill=(0, 0, 0))  # Màu viền là đen

        # Vẽ chữ chính
        draw.text((x, y), char, font=font, fill=char_color)
        
        char_width = draw.textbbox((0, 0), char, font=font)[2]
        x += char_width

# Hàm tạo ảnh chào mừng hoặc tiễn biệt
def create_welcome_or_farewell_image(group_name, member_name, avatar_url, event_type):
    background = create_black_background(736, 282)
    draw = ImageDraw.Draw(background)

    avatar_response = requests.get(avatar_url)
    avatar_response.raise_for_status()
    avatar = Image.open(BytesIO(avatar_response.content)).convert("RGBA")
    avatar = avatar.resize((150, 150), Image.LANCZOS)
    round_avatar = make_round_avatar(avatar)
    avatar_x = 30
    avatar_y = (background.height - round_avatar.height) // 2
    background.paste(round_avatar, (avatar_x, avatar_y), round_avatar)

    line_x = avatar_x + round_avatar.width + 25
    draw.line([(line_x, avatar_y - 40), (line_x, avatar_y + round_avatar.height + 40)], fill="white", width=4)

    # Xử lý text dựa trên loại sự kiện
    if event_type == "JOIN":
        text_group = f"{member_name} vừa tham gia Group!"
        text_member = f"Chào Mừng!"
    elif event_type == "LEAVE":
        text_group = f"{member_name} vừa rời khỏi Group!"
        text_member = f"Bye Con Chó Ngu!"
    elif event_type == "REMOVE_MEMBER":
        text_group = f"{member_name} đã bị xóa khỏi Group!"
        text_member = f"Ngu thì cút!"
    else:
        text_group = "Sự kiện không xác định!"
        text_member = f"Xin chào!"

    font_path_group = "font/UTM Avo.ttf"
    font_path_member = "font/NotoSans-Bold.ttf"
    font_path_signature = "font/UTM Avo.ttf"

    max_text_width = background.width - round_avatar.width - 150
    font_group = adjust_font_size(draw, text_group, max_width=max_text_width, font_path=font_path_group, initial_size=33)
    font_member = adjust_font_size(draw, text_member, max_width=max_text_width, font_path=font_path_member, initial_size=30)
    font_signature = ImageFont.truetype(font_path_signature, 30)

    text_group_y = (background.height - 150) // 2 + 60
    signature_y_group = text_group_y + 90
    text_member_y = text_group_y - 50

    gradient_colors = create_gradient_colors(5)

    # Vẽ chữ có viền
    draw_text_with_border(draw, text_group, position=(230, text_group_y), font=font_group, gradient_colors=gradient_colors)
    draw_text_with_border(draw, "by.nttiue", position=(500, signature_y_group), font=font_signature, gradient_colors=gradient_colors)
    draw_text_with_border(draw, text_member, position=(230, text_member_y), font=font_member, gradient_colors=gradient_colors)

    image_path = "welcome_or_farewell.jpg"
    background.save(image_path)
    return image_path

# Xóa file
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Đã xóa file: {file_path}")
        else:
            print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        logging.error(f"Lỗi khi xóa file {file_path}: {e}")

# Chức năng chào mừng hoặc tiễn biệt
def welcome(self, event_data, event_type, ttl=60000):
    def send():
        if event_type == GroupEventType.UNKNOWN:
            return

        thread_id = event_data['groupId']
        group_info = self.fetchGroupInfo(thread_id)
        if not group_info or 'gridInfoMap' not in group_info or thread_id not in group_info.gridInfoMap:
            print(f"Không thể lấy thông tin nhóm cho thread_id: {thread_id}")
            return

        group_name = group_info.gridInfoMap[thread_id]['name']

        if event_type == GroupEventType.JOIN:
            for member in event_data.updateMembers:
                member_name = member['dName']
                avatar_url = member.get('avatar', '')

                welcome_image_path = create_welcome_or_farewell_image(group_name, member_name, avatar_url, "JOIN")
                self.sendLocalImage(
                    welcome_image_path, 
                    thread_id, 
                    ThreadType.GROUP, 
                    message=None, 
                    width=600, 
                    height=225, 
                    ttl=ttl
                )
                delete_file(welcome_image_path)

        elif event_type == GroupEventType.LEAVE:
            for member in event_data.updateMembers:  # Thêm vòng lặp để xử lý từng thành viên
                member_name = member['dName']
                avatar_url = member.get('avatar', '')

                farewell_image_path = create_welcome_or_farewell_image(group_name, member_name, avatar_url, "LEAVE")
                self.sendLocalImage(
                    farewell_image_path, 
                    thread_id, 
                    ThreadType.GROUP, 
                    message=None, 
                    width=600, 
                    height=225, 
                    ttl=ttl
                )
                delete_file(farewell_image_path)

        elif event_type == GroupEventType.REMOVE_MEMBER:
            for member in event_data.updateMembers:
                member_name = member['dName']
                avatar_url = member.get('avatar', '')

                kick_image_path = create_welcome_or_farewell_image(group_name, member_name, avatar_url, "REMOVE_MEMBER")
                self.sendLocalImage(
                    kick_image_path, 
                    thread_id, 
                    ThreadType.GROUP, 
                    message=None, 
                    width=600, 
                    height=225, 
                    ttl=ttl
                )
                delete_file(kick_image_path)

    thread = Thread(target=send)
    thread.daemon = True
    thread.start()
def get_mitaizl():
    return {}