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

# HÀM TẢI AVATAR 
def ping(message, message_object, thread_id, thread_type, author_id, client):
    image_dir = "background"
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("Không tìm thấy ảnh trong thư mục background!")
        return

    random_image = random.choice(image_files)
    image_path = os.path.join(image_dir, random_image)
    output_image_path = "output.png"
    
    size = (1124, 402)
    box_color = (0, 0, 0, 150)
    
    bg_image = Image.open(image_path).convert("RGBA").resize(size).filter(ImageFilter.GaussianBlur(8))
    overlay = Image.new("RGBA", size, (0))
    draw = ImageDraw.Draw(overlay)
    
    box_x1, box_y1 = 50, 30
    box_x2, box_y2 = size[0] - 50, size[1] - 30
    draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=35, fill=box_color)
    
    font_path = "font/arial.ttf"
    font_text = ImageFont.truetype(font_path, 42) if os.path.exists(font_path) else ImageFont.load_default()
    font_time = ImageFont.truetype(font_path, 38) if os.path.exists(font_path) else ImageFont.load_default()
    font_emoji_path = "font/noto-emoji-bold.ttf"
    font_icon = ImageFont.truetype(font_emoji_path, 150) if os.path.exists(font_emoji_path) else ImageFont.load_default()
    
    vietnam_now = datetime.now(timezone(timedelta(hours=7)))
    formatted_time = vietnam_now.strftime("%H:%M")
    draw.text((box_x2 - 140, box_y1 + 5), formatted_time, font=font_time, fill=(255, 255, 255))
    
    text_lines = [
       f"Hi, Tôi Là Bot",
       f"Chào Mừng Đến Với Menu",
        "                                                         ",
       f"Bot Luôn Sẵn Sàng Phục Vụ Bạn",
       f"Duy Khanh | Version 0.0.1 | Update 10/5/2025"
    ]

    # Tạo một mask màu trắng cho các dòng chữ
    text_colors = [(255, 255, 255), (255, 215, 0), (50, 205, 50), (255, 69, 0), (30, 144, 255)]
    
    for i, line in enumerate(text_lines):
        text_x = (box_x1 + box_x2) // 2 - len(line) * 10
        text_y = box_y1 + 70 + i * 50
        draw.text((text_x, text_y), line, font=font_text, fill=text_colors[i])
    
    random_icons = ["⚙️", "🎮", "💝", "⭐", "🚀", "🎭", "🎶"]
    draw.text((box_x1 + 30, (box_y1 + box_y2) // 2 - 90), random.choice(random_icons), font=font_icon, fill=(30, 144, 255))
    draw.text((box_x2 - 180, (box_y1 + box_y2) // 2 - 90), random.choice(random_icons), font=font_icon, fill=(255, 69, 0))
    
    combined = Image.alpha_composite(bg_image, overlay)
    combined.save(output_image_path, format="PNG")
    
    # Chuẩn bị văn bản trong text
    text = f"""🚦@member
 • Menu Bot •
 
   ➜🔥 [Bot-group] Quản lý Group
   ➜👽 [War] Lệnh War2
   ➜💨 [Stk] Tạo Sticker
   ➜🎸 [Nhạc] Chọn Nhạc
   ➜💋 [uptcard] Card cá nhân
   ➜🤭 [tangai] Thả thính
   ➜🌊 [Alo] Gọi Bot
   ➜💵 [Reo] War Tag
   ➜🧭 [Kdl] Khởi Tạo Lại Bot
   ➜🤖 [qrcode] Tạo mã qc
   ➜🤖 [scanqr] scan qrcode
   ➜📝 [delall] Xoá tin nhắn
   ➜🎨 [Taoanh] Vẽ ảnh (make)
   ➜🌐 [Voice] Tạo Voice
   ➜🖼️ [Bantho] Bàn thờ @user
   ➜💻 [Uptime] Thời Gian Chạy Bot
   ➜👤 [advip] Thông tin ADMIN
   ➜🌼 [ktra] Pinging Check Độ trễ
   ➜🗣 [tagall] Gọi chó
   ➜🌡 [thoitiet] Thông báo thời tiết
   ➜☎ [spamsms] Spam SMS
   ➜🔞 [vdsex] Video gái🔞
   ➜🐰 [vd18] Video ...
   ➜👩‍💼 [girl] Ảnh gái
   ➜🙎 [nude] Ảnh nude🔞
   ➜🦄 [sexv4] vd sex🔞
   ➜🏝 [animegura] Ảnh animegura
   ➜🌊  [chill] Gửi vd chill
   ➜🌅 [meme] Ảnh meme
   ➜📀 [vdgirl] Video gái
   ➜🗻 [animechill] Gửi vd anime chill
   ➜🎮 [txiu] Game
   ➜📺 [gpt] Chat gpt 5.0
   ➜🖥 [rs] Reset bot
   ➜💌 [warpoll] spam tạo bình chọn
   ➜🎭 [meid] Lấy id @user
   ➜☀ [media] Gửi ảnh từ link
   ➜🍾 [chuctet] Chúc tết
   ➜🍼 [chucngungon] Chúc ngủ ngon
   ➜💑 [chucvuive] Chúc vui vẻ
   ➜👻 [bot] Gọi bot
   ➜🍷 [boibai] Xem bói
   ➜🏘 [cap] Cap lại web
   ➜👾 [auto_on] auto thính
   ➜🚨 [chui1-52] spam chửi
   ➜👩‍💼 [duyetmen] Duyệt men
    𝗔𝗗𝗠𝗜𝗡 : 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜
 
"""
    action = "⚙️"
    client.sendReaction(message_object, action, thread_id, thread_type, reactionType=75)
    client.sendLocalImage(
        imagePath=output_image_path,
        message=Message(text=text, mention=Mention(author_id, offset=len("🚦 "), length=len("@member"))),
        thread_id=thread_id,
        thread_type=thread_type,
        width=1124,
        height=402,
        ttl=300000
    )

def get_mitaizl():
    return {
        'menu2': ping
    }
