import requests
import os
from datetime import datetime
from zlapi.models import Message, ZaloAPIException
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Troll bàn thờ(tag)"
}

def create_canvas(user_data):
    background_image = Image.open("bantho.jpeg")
    draw = ImageDraw.Draw(background_image)

    bg_width, bg_height = background_image.size

    avatar_url = user_data.get('avatar')
    avatar_image = None
    if avatar_url:
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        avatar_image = Image.open("default_avatar.jpg").convert("RGB")

    avatar_size = (425, 565) #size avt (YHT)
    avatar_image = ImageOps.fit(avatar_image, avatar_size, centering=(0.5, 0.5))

    mask = Image.new("L", avatar_size, 255) #góc bo tròn - vuông (YHT)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + avatar_size, fill=255) #độ mờ avt (YHT)

    avatar_image.putalpha(mask)

    avatar_x = bg_width - avatar_size[0] - 1127
    avatar_y = (bg_height - avatar_size[1]) // 3
    
    background_image.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

    fontc = "UTM AvoBold.ttf"

    font_title = ImageFont.truetype(fontc, 80)
    font_info = ImageFont.truetype(fontc, 80)
    font_bio = ImageFont.truetype(fontc, 30)

    draw.text((700, 1000), "Chia buồn cùng gia đình", font=font_title, fill=(300, 300, 300))
    draw.text((1150, 1100), user_data.get('displayName', 'N/A'), font=font_info, fill=(300, 300, 300))
    
    canvas_path = "output_canvas.png"
    background_image.save(canvas_path)
    return canvas_path
    
def handle_user_info(message, message_object, thread_id, thread_type, author_id, client):
    try:
        input_value = message.split()[1].lower() if len(message.split()) > 1 else author_id

        if message_object.mentions:
            input_value = message_object.mentions[0]['uid']

        user_id_data = client.fetchPhoneNumber(input_value, language="vi") or {}
        user_id_to_fetch = user_id_data.get('uid', input_value)
        sdob_to_fetch = user_id_data.get('sdob')

        user_info = client.fetchUserInfo(user_id_to_fetch) or {}
        user_data = user_info.get('changed_profiles', {}).get(user_id_to_fetch, {})

        canvas_path = create_canvas(user_data) 
        if os.path.exists(canvas_path):
            client.sendLocalImage(
                canvas_path, 
                message=None,
                thread_id=thread_id,
                thread_type=thread_type,
                width=2323,
                height=1039,
                ttl=120000
            )
            confirmation_message = Message(text="Đã gửi ảnh người mất☠️.")
            client.replyMessage(confirmation_message, message_object, thread_id, thread_type,ttl=120000)
            
            os.remove(canvas_path)

    except (ValueError, ZaloAPIException) as e:
        error_message = Message(text=f"Error: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id, thread_type,ttl=10000)
    except Exception as e:
        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id, thread_type,ttl=10000)

def get_mitaizl():
    return {
        'bantho': handle_user_info
    }