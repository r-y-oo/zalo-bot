import sys
import os
import time
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from zlapi.models import Message, MultiMsgStyle, MessageStyle, Mention, ThreadType
from config import ADMIN

ADMIN_ID = ADMIN

des = {
    'version': "1.2.0",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Restart lại bot và gửi ảnh"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def create_multicolor_gradient(width, height, num_colors=20):
    base = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    colors = [
        (0, random.randint(100, 255), random.randint(100, 255), 255),
        (random.randint(100, 255), 0, random.randint(100, 255), 255),
        (random.randint(100, 255), 0, 0, 255),
        (0, random.randint(100, 255), 0, 255),
        (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 255)
    ]
    segment_width = width // (len(colors) - 1)
    for i in range(len(colors) - 1):
        start_color = colors[i]
        end_color = colors[i + 1]
        for x in range(i * segment_width, (i + 1) * segment_width):
            ratio = (x - i * segment_width) / segment_width
            blended_color = tuple(
                int(start_color[j] * (1 - ratio) + end_color[j] * ratio) for j in range(3)
            ) + (255,)
            draw.line([(x, 0), (x, height)], fill=blended_color)
    return base.filter(ImageFilter.GaussianBlur(radius=15))

def get_font_size(content, image_width):
    max_font_size = 120
    min_font_size = 10
    font_path = "font/UTM AvoBold_Italic.ttf"

    for size in range(max_font_size, min_font_size, -2):
        font = ImageFont.truetype(font_path, size)
        text_width = sum(font.getbbox(char)[2] for char in content)
        if text_width < image_width * 0.9:
            return font
    return ImageFont.truetype(font_path, min_font_size)

def draw_text_with_gradient(image, text, position, font):
    mask = Image.new("L", (image.width, image.height), 0)
    draw = ImageDraw.Draw(mask)
    draw.text(position, text, font=font, fill=255)

    gradient = create_multicolor_gradient(image.width, image.height)
    image.paste(gradient, (0, 0), mask)

    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.text((position[0] + 5, position[1] + 5), text, font=font, fill=(0, 0, 0, 180))
    image.paste(shadow, (0, 0), shadow)

    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.text(position, text, font=font, fill=(255, 255, 255, 100))
    image.paste(glow, (0, 0), glow)

def create_galaxy_gradient(width, height):
    base = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(base)

    colors = [
        (20, 20, 50, 255),
        (75, 0, 130, 255),
        (138, 43, 226, 255),
        (255, 20, 147, 255),
        (255, 69, 0, 255)
    ]

    for i in range(len(colors) - 1):
        start_color = colors[i]
        end_color = colors[i + 1]
        for x in range(i * (width // (len(colors) - 1)), (i + 1) * (width // (len(colors) - 1))):
            ratio = (x - i * (width // (len(colors) - 1))) / (width // (len(colors) - 1))
            blended_color = tuple(
                int(start_color[j] * (1 - ratio) + end_color[j] * ratio) for j in range(3)
            ) + (255,)
            draw.line([(x, 0), (x - width, height)], fill=blended_color)

    base = base.filter(ImageFilter.GaussianBlur(radius=20))

    star_draw = ImageDraw.Draw(base)
    for _ in range(200):
        x, y = random.randint(0, width), random.randint(0, height)
        size = random.randint(1, 3)
        star_draw.ellipse((x, y, x + size, y + size), fill=(255, 255, 255, random.randint(150, 255)))

    return base

def handle_reset_command(message, message_object, thread_id, thread_type, author_id, client):
    if not is_admin(author_id):
        msg = "•🚦𝙈𝙖̀𝙮 𝙠𝙝𝙤̂𝙣𝙜 𝙘𝙤́ 𝙦𝙪𝙮𝙚̂̀𝙣 𝙨𝙪̛̉ 𝙙𝙪̣𝙣𝙜 𝙡𝙚̣̂𝙣𝙝 𝙣𝙖̀𝙮 𝙘𝙝𝙞̉ 𝙘𝙤́ 𝙘𝙤́ 𝙖𝙙𝙢𝙞𝙣 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 𝙢𝙤̛́𝙞 𝙨𝙖̀𝙞 𝙙𝙪̛𝙤̛̣𝙘 !🔱"
        client.replyMessage(Message(text=msg), message_object, thread_id, thread_type)
        return
    try:
        # Gửi 8 icon reaction ngẫu nhiên từ icon_list
        icon_list = [
            "🔥", "💎", "🚀", "🎮", "✨", "📜", "🛠️", "🌟", "💖", "⚡",
            "🐉", "🎭", "🕹️", "💡", "🎤", "🥇", "🎲", "🧩", "🎯", "🔮",
            "📢", "💬", "🌍", "📝", "🎨", "🎶", "🎵", "🎷", "🎺", "🥁", 
            "🦅", "🥀", "👿", "👹", "👺", "💀", "👻", "👽", "🤖", "💩"
        ]
        random_emojis = random.sample(icon_list, 8)
        for emoji in random_emojis:
            try:
                client.sendReaction(message_object, emoji, thread_id, thread_type, reactionType=75)
            except Exception as e:
                print(f"Lỗi khi gửi phản ứng {emoji}: {e}")

        # Gửi tin nhắn thông báo restart bot
        client.sendMessage(Message(text="💨 𝙷𝚎̣̂ 𝚝𝚑𝚘̂́𝚗𝚐 𝚍𝚊𝚗𝚐 𝚌𝚑𝚞𝚊̂̉𝚗 𝚋𝚒̣ 𝚛𝚎𝚜𝚎𝚝 𝚋𝚘𝚝... 𝚅𝚞𝚒 𝚕𝚘̀𝚗𝚐 𝚌𝚑𝚘̛̀ 𝚐𝚒𝚊̂𝚢 𝚕𝚊́𝚝🔱"), thread_id, thread_type)

        # Tạo ảnh thông báo
        content = "Duy Khanh!!, Đang Setup Lại Bot !!"
        image_width, image_height = 800, 333
        image = create_galaxy_gradient(image_width, image_height)
        font = get_font_size(content, image_width)

        bbox = ImageDraw.Draw(image).textbbox((0, 0), content, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2

        draw_text_with_gradient(image, content, (x, y), font)

        output_path = "modules/cache/temp_image_with_text.png"
        image.save(output_path)

        # Gửi ảnh sau khi đã thả icon và gửi tin nhắn
        if os.path.exists(output_path):
            client.sendLocalImage(
                output_path,
                message=Message(text="@Member 🚦 𝙳𝚊𝚗𝚐 𝚁𝚎𝚜𝚎𝚝 𝚃𝚑𝚞̛𝚊 Duy Khanh⚜️", mention=Mention(author_id, length=len("@Member"), offset=0)),
                thread_id=thread_id,
                thread_type=thread_type,
                width=800,
                height=333
            )
            os.remove(output_path)

        # Lưu thông tin restart
        with open("modules/cache/restart_info.txt", "w") as f:
            f.write(f"{thread_id}\n{thread_type.name}")

        time.sleep(0)

        # Thực hiện restart bot
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception as e:
        client.replyMessage(Message(text=f"• Đã xảy ra lỗi khi restart bot: {str(e)}"), message_object, thread_id, thread_type)

def send_reset_success_message(client):
    try:
        with open("modules/cache/restart_info.txt", "r") as f:
            lines = f.readlines()
            thread_id = lines[0].strip()
            thread_type = ThreadType[lines[1].strip()]

        success_message = Message(text="🚦 Bot đã được reset thành công! Hệ thống đã hoạt động trở lại🌹.")
        client.sendMessage(success_message, thread_id, thread_type)

        os.remove("modules/cache/restart_info.txt")
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn xác nhận sau khi restart: {e}")

def get_mitaizl():
    return {
        'rs': handle_reset_command
    }