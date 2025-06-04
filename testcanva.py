import time
import os
import random
from PIL import Image, ImageDraw, ImageFont
from zlapi.models import Message, Mention

des = {
    'version': "4.0.9",
    'credits': "Dzi on the mine",
    'description': "Tạo ảnh nền với màu RGB và tự động điều chỉnh kích thước chữ"
}

def create_rgb_colors(width, height, num_colors):
    colors = []
    for i in range(num_colors):
        color = (
            random.randint(100, 175),
            random.randint(100, 180),
            random.randint(100, 170)
        )
        colors.append(color)
    return colors

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

def draw_text(draw, text, position, font, gradient_fill):
    x, y = position
    offset = 1

    for index, char in enumerate(text):
        for dx in [-offset, 0, offset]:
            for dy in [-offset, 0, offset]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), char, fill=(0, 0, 0), font=font)

        draw.text((x, y), char, fill=gradient_fill[index], font=font)

        x += draw.textbbox((x, y), char, font=font)[2] - draw.textbbox((x, y), char, font=font)[0]

def get_font_size(content, image_width):
    max_font_size = 100
    min_font_size = 10  # Ensure there's a minimum font size
    font_path = "UTMAvoBold.ttf"

    for size in range(max_font_size, min_font_size, -2):
        font = ImageFont.truetype(font_path, size)
        text_width = sum(font.getbbox(char)[2] for char in content)
        if text_width < image_width * 0.9:
            return font
    return ImageFont.truetype(font_path, min_font_size)

def handle_create_image_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        text = message.split(" ", 1)
        if len(text) < 2:
            client.replyMessage(Message(text="@Member, vui lòng cung cấp nội dung cần tạo ảnh !", mention=Mention(author_id, length=len("@Member"), offset=0)), message_object, thread_id, thread_type)
            return

        content = text[1]
        image_width, image_height = 800, 333
        rgb_colors = create_rgb_colors(image_width, image_height, num_colors=5)
        gradient_fill = interpolate_colors(rgb_colors, len(content))
        image = Image.new("RGB", (image_width, image_height), color=(30,30,30))
        draw = ImageDraw.Draw(image)
        font = get_font_size(content, image_width)
        bbox = draw.textbbox((0, 0), content, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2
        draw_text(draw, content, (x, y), font, gradient_fill)
        output_path = "modules/cache/temp_image_with_text.jpg"
        image.save(output_path)
        if os.path.exists(output_path):
            client.sendLocalImage(
                output_path,
                message=Message(text="@Member", mention=Mention(author_id, length=len("@Member"), offset=0)),
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=86400000,
                width=800,
                height=333
            )
           # Thông báo sau khi video đã được gửi
            found_message = ""
            client.send(
            Message(text=found_message),
            thread_id=thread_id,
            thread_type=thread_type, ttl=86400000
            )         
            os.remove(output_path)
        else:
            raise Exception("Không thể lưu ảnh.")

    except Exception as e:
        client.sendMessage(Message(text=f"Đã xảy ra lỗi: {str(e)}"), thread_id, thread_type)

def get_mitaizl():
    return {
        'canva': handle_create_image_command
    }