import json
import random
from zlapi.models import *

def create_rainbow_params(text, size=20):
    styles = []
    colors = generate_gradient_colors(len(text))
    
    for i, color in enumerate(colors):
        styles.append({"start": i, "len": 1, "st": f"c_{color}"})
        # styles.append({"start": i, "len": 1, "st": f"c_{color},f_{size}"})
    
    params = {"styles": styles, "ver": 0}
    return json.dumps(params)



def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '{:02x}{:02x}{:02x}'.format(*rgb_color)

def generate_random_color():
    """Tạo một mã màu hex ngẫu nhiên."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def generate_complementary_color(hex_color):
    """Tạo màu tương phản (complementary) từ một mã màu hex."""
    rgb = hex_to_rgb(hex_color)
    # Màu tương phản được tính bằng cách lấy 255 trừ đi từng kênh màu (RGB)
    complementary_rgb = (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])
    return rgb_to_hex(complementary_rgb)

def generate_gradient_colors(length):
    start_color = generate_random_color()
    end_color = generate_random_color()
    # end_color = generate_complementary_color(start_color)
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    colors = []
    for i in range(length):
        interpolated_color = (
            int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (length - 1)),
            int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (length - 1)),
            int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (length - 1))
        )
        colors.append(rgb_to_hex(interpolated_color))
    
    return colors

def sendMessageColor(message, message_object, thread_id, thread_type, author_id, client):
    if len(custom_text)<=77:
        stype=create_rainbow_params(custom_text)
        # print(len(custom_text),"\n", stype)
        # Xử lý nội dung custom_text theo yêu cầu
        mes=Message(
            text=custom_text,
            style=stype
        )
        client.send( mes, thread_id, thread_type)
    else:
        client.send( Message(text=f"{custom_text}"), thread_id, thread_type)

def replyMessageColor(message, message_object, thread_id, thread_type, author_id, client):
    custom_text = message.split(' ', 1)[1].strip() if len(message.split(' ', 1)) > 1 else ""
    if len(custom_text)<=77:
        stype=create_rainbow_params(custom_text)
        # print(stype)
        # print(len(custom_text))
        #gioi han chi duoc 77 chu
        mes=Message(
            text=custom_text,
            style=stype
        )
        client.replyMessage(mes, message_object, thread_id=thread_id, thread_type=thread_type)
    else:
        client.replyMessage(Message(text=f"{custom_text}"), message_object, thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'text': replyMessageColor
    }
