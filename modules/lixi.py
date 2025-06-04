import json
import os
import random
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from zlapi import *
from zlapi.models import *
from fake_useragent import UserAgent
from config import API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES

# Function for generating random RGB colors
def create_rgb_colors(width, height, num_colors):
    colors = []
    for i in range(num_colors):
        color = (
            random.randint(100, 300),
            random.randint(100, 300),
            random.randint(100, 300)
        )
        colors.append(color)
    return colors

# Interpolate colors for gradient effect
def interpolate_colors(colors, text_length):
    gradient = []
    num_segments = len(colors) - 1
    steps_per_segment = (text_length // len(colors)) + 1

    for i in range(num_segments):
        for j in range(steps_per_segment):
            if len(gradient) < text_length:
                ratio = j / steps_per_segment
                interpolated_color = (
                    int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio),
                    int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio),
                    int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                )
                gradient.append(interpolated_color)

    while len(gradient) < text_length:
        gradient.append(colors[-1])

    return gradient[:text_length]

# Function to draw the text with a gradient color
def draw_text(draw, text, position, fonts, gradient_fill):
    x, y = position
    offset = 1

    # Loop through each character and draw it
    for index, char in enumerate(text):
        font = fonts['UTM'] if char.isalnum() else fonts['NotoEmoji']
        for dx in [-offset, 0, offset]:
            for dy in [-offset, 0, offset]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), char, fill=(0, 0, 0), font=font)

        draw.text((x, y), char, fill=gradient_fill[index], font=font)

        # Update the position for the next character
        x += draw.textbbox((x, y), char, font=font)[2] - draw.textbbox((x, y), char, font=font)[0]

# Function to get the appropriate font size based on content length
def get_font_size(content, image_width, fonts):
    max_font_size = 90
    min_font_size = 10
    font = fonts['UTM']

    for size in range(max_font_size, min_font_size, -2):
        fonts['UTM'] = ImageFont.truetype("modules/utm-avo/UTM-AvoBold.ttf", size)
        fonts['NotoEmoji'] = ImageFont.truetype("modules/utm-avo/NotoEmoji-Bold.ttf", size)
        text_width = sum(fonts['UTM'].getbbox(char)[2] if char.isalnum() else fonts['NotoEmoji'].getbbox(char)[2] for char in content)
        if text_width < image_width * 0.9:
            return fonts
    fonts['UTM'] = ImageFont.truetype("modules/utm-avo/UTM-AvoBold.ttf", min_font_size)
    fonts['NotoEmoji'] = ImageFont.truetype("modules/utm-avo/NotoEmoji-Bold.ttf", min_font_size)
    return fonts

# Function to send voice message
def send_local_audio(file_path, thread_id, thread_type, client):
    """Gửi âm thanh từ máy tính."""
    try:
        # Gửi âm thanh từ máy tính
        client.sendLocalVoice(file_path, thread_id, thread_type)
        print("Gửi âm thanh thành công từ máy tính!")
    except Exception as e:
        print(f"Lỗi khi gửi âm thanh: {e}")

# Function to handle lixi command
def handle_lixi_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        text = message.split(" ", 1)
        if len(text) < 2:
            client.replyMessage(
                Message(
                    text="@Member, vui lòng cung cấp tên chỉ được 1 từ thôi bạn nhé ví dụ .lixi tên!",
                    mention=Mention(author_id, length=len("@Member"), offset=0)
                ),
                message_object, thread_id, thread_type
            )
            return

        content = text[1]

        # Tính toán kích thước ảnh theo nội dung
        image_width = max(400, len(content) * 15)  # Mở rộng chiều rộng ảnh dựa trên độ dài nội dung
        image_height = 1000  # Chiều cao lớn hơn để ảnh thành hình chữ nhật

        # Tải ảnh nền
        background_path = "modules/cache/lx.jpg"  # Đường dẫn tới ảnh nền
        if not os.path.exists(background_path):
            raise Exception("Ảnh nền không tồn tại.")
        
        # Tải ảnh nền và resize
        background_image = Image.open(background_path).convert("RGB")
        background_image = background_image.resize((image_width, image_height))

        # Vẽ lên ảnh nền
        draw = ImageDraw.Draw(background_image)

        # Tạo gradient màu cho text
        rgb_colors = create_rgb_colors(image_width, image_height, num_colors=5)
        gradient_fill = interpolate_colors(rgb_colors, len(content))

        # Tải font
        fonts = {
            'UTM': ImageFont.truetype("modules/utm-avo/UTM-AvoBold.ttf", 20),
            'NotoEmoji': ImageFont.truetype("modules/utm-avo/NotoEmoji-Bold.ttf", 20)
        }
        fonts = get_font_size(content, image_width, fonts)

        # Căn chỉnh chữ ở phía trên của ảnh
        text_width = sum(fonts['UTM'].getbbox(char)[2] if char.isalnum() else fonts['NotoEmoji'].getbbox(char)[2] for char in content)
        text_height = max(fonts['UTM'].getbbox(char)[3] for char in content)
        x = (image_width - text_width) // 2  # Căn giữa theo chiều ngang
        y = 160  # Căn trên, cách 20px từ trên cùng

        # Vẽ text lên ảnh nền
        draw_text(draw, content, (x, y), fonts, gradient_fill)

        # Thêm dòng chữ "Chúc mừng năm mới" ở dưới
        new_year_text = "Chúc mừng năm mới "
        
        # Phóng to kích thước chữ cho dòng năm mới
        new_year_fonts = {
            'UTM': ImageFont.truetype("modules/utm-avo/UTM-AvoBold.ttf", 25),
            'NotoEmoji': ImageFont.truetype("modules/utm-avo/NotoEmoji-Bold.ttf", 25)
        }

        # Tính toán kích thước của chữ năm mới với kích thước phóng to
        new_year_text_width = sum(new_year_fonts['UTM'].getbbox(char)[2] for char in new_year_text)
        new_year_text_height = max(new_year_fonts['UTM'].getbbox(char)[3] for char in new_year_text)

        # Duyệt chiều cao ảnh và căn chỉnh vị trí cho chữ năm mới
        max_available_y = image_height - new_year_text_height - 400  # Dưới cùng của ảnh
        new_year_x = (image_width - new_year_text_width) // 3
        new_year_y = max_available_y  # Đảm bảo căn dưới cùng

        # Tạo gradient cho dòng chữ năm mới
        new_year_gradient_fill = interpolate_colors(rgb_colors, len(new_year_text))
        draw_text(draw, new_year_text, (new_year_x, new_year_y), new_year_fonts, new_year_gradient_fill)

        # Thêm dòng chữ "2025" ở dưới dòng "Chúc mừng năm mới"
        year_text = "2025"
        
        # Phóng to chữ "2025" sao cho vừa với ảnh
        max_font_size = 100
        min_font_size = 30
        year_fonts = None
        for size in range(max_font_size, min_font_size, -2):
            temp_fonts = {
                'UTM': ImageFont.truetype("modules/utm-avo/UTM-AvoBold.ttf", size),
                'NotoEmoji': ImageFont.truetype("modules/utm-avo/NotoEmoji-Bold.ttf", size)
            }
            year_text_width = sum(temp_fonts['UTM'].getbbox(char)[2] for char in year_text)
            if year_text_width < image_width * 0.9:
                year_fonts = temp_fonts
                break

        # Tính toán vị trí của chữ "2025"
        year_text_width = sum(year_fonts['UTM'].getbbox(char)[2] for char in year_text)
        year_text_height = max(year_fonts['UTM'].getbbox(char)[3] for char in year_text)
        
        year_x = (image_width - year_text_width) // 2
        year_y = new_year_y + new_year_text_height  # Dưới chữ "Chúc mừng năm mới"

        # Tạo gradient cho dòng chữ "2025"
        year_gradient_fill = interpolate_colors(rgb_colors, len(year_text))
        draw_text(draw, year_text, (year_x, year_y), year_fonts, year_gradient_fill)

        # Lưu ảnh kết quả
        output_path = "modules/cache/temp_image_with_text.jpg"
        background_image.save(output_path)

        if os.path.exists(output_path):
            client.sendLocalImage(
                output_path,
                message=Message(text="@Member năm mới vui vẻ, cung hỷ phát tài", mention=Mention(author_id, length=len("@Member"), offset=0)),
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=86400000,
                width=image_width,
                height=image_height
            )
            # Send voice message after sending image
            audio_url = "https://fg40.dlfl.me/e0b3730ae4a74af913b6/4828461272794283869"
            client.sendRemoteVoice(voiceUrl=audio_url, thread_id=thread_id, thread_type=thread_type)
            os.remove(output_path)
        else:
            raise Exception("Không thể lưu ảnh.")

    except Exception as e:
        client.sendMessage(Message(text=f"Đã xảy ra lỗi: {str(e)}"), thread_id, thread_type)

# Function to get the commands for bot
def get_mitaizl():
    return {
        'lixi': handle_lixi_command
    }
