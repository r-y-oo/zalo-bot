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
from config import PREFIX, ADMIN

def create_menu_image():
    """Tạo ảnh menu với background random"""
    try:
        image_dir = "background"
        if not os.path.exists(image_dir):
            return None
            
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            return None

        random_image = random.choice(image_files)
        image_path = os.path.join(image_dir, random_image)
        output_image_path = "menu_output.png"
        
        size = (1200, 800)
        box_color = (0, 0, 0, 160)
        
        bg_image = Image.open(image_path).convert("RGBA").resize(size).filter(ImageFilter.GaussianBlur(12))
        overlay = Image.new("RGBA", size, (0))
        draw = ImageDraw.Draw(overlay)
        
        # Main box
        box_x1, box_y1 = 40, 40
        box_x2, box_y2 = size[0] - 40, size[1] - 40
        draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=25, fill=box_color)
        
        # Title box
        title_y2 = box_y1 + 100
        draw.rounded_rectangle([(box_x1 + 20, box_y1 + 20), (box_x2 - 20, title_y2)], radius=15, fill=(30, 144, 255, 200))
        
        # Load fonts
        font_path = "font/arial.ttf"
        title_font = ImageFont.truetype(font_path, 48) if os.path.exists(font_path) else ImageFont.load_default()
        subtitle_font = ImageFont.truetype(font_path, 24) if os.path.exists(font_path) else ImageFont.load_default()
        
        # Time
        vietnam_now = datetime.now(timezone(timedelta(hours=7)))
        formatted_time = vietnam_now.strftime("%d/%m/%Y %H:%M")
        
        # Title
        title_text = "🤖 BOT MENU SYSTEM"
        draw.text((size[0]//2 - 200, box_y1 + 35), title_text, font=title_font, fill=(255, 255, 255))
        draw.text((size[0]//2 - 80, title_y2 - 35), formatted_time, font=subtitle_font, fill=(255, 255, 255))
        
        combined = Image.alpha_composite(bg_image, overlay)
        combined.save(output_image_path, format="PNG")
        
        return output_image_path
        
    except Exception as e:
        print(f"Lỗi tạo ảnh menu: {e}")
        return None

def show_main_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Hiển thị menu chính với các danh mục"""
    
    # Tạo ảnh menu
    image_path = create_menu_image()
    
    text = f"""🚦 @member
╭─────────────────────────╮
│       🤖 BOT MENU SYSTEM       │
╰─────────────────────────╯

📂 DANH MỤC LỆNH:

🔧 QUẢN LÝ & ADMIN
   {PREFIX}admin - Quản lý admin
   {PREFIX}menua - Lệnh admin

👥 QUẢN LY GROUP  
   {PREFIX}menug - Lệnh group
   {PREFIX}bot-group - Quản lý group

🎮 GIẢI TRÍ & GAME
   {PREFIX}menuf - Lệnh giải trí
   {PREFIX}txiu - Game

🎵 ÂM NHẠC & MEDIA
   {PREFIX}menum - Lệnh âm nhạc
   {PREFIX}nhac - Chọn nhạc

🖼️ ẢNH & VIDEO
   {PREFIX}menuv - Lệnh ảnh/video
   {PREFIX}girl - Ảnh gái

🔞 CONTENT 18+
   {PREFIX}menu18 - Lệnh 18+
   {PREFIX}vdsex - Video 18+

🛠️ CÔNG CỤ & TIỆN ÍCH
   {PREFIX}menut - Công cụ
   {PREFIX}qrcode - Tạo QR

🌐 MẠNG XÃ HỘI
   {PREFIX}menus - Social media
   {PREFIX}spamsms - Spam SMS

💬 CHAT & AI
   {PREFIX}menuc - Chat AI
   {PREFIX}gpt - ChatGPT

📊 THỐNG KÊ & INFO
   {PREFIX}stats - Thống kê bot
   {PREFIX}uptime - Thời gian chạy

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 LỆNH NHANH (KHÔNG PREFIX):
   hello, hi, chào - Chào hỏi
   bot, bót - Gọi bot  
   system - Thông tin hệ thống

💡 TIP: Gõ tên danh mục để xem chi tiết!
━━━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 ADMIN: Hà Huy Hoàng | v2.1.0
"""

    # React và gửi
    client.sendReaction(message_object, "⚙️", thread_id, thread_type, reactionType=75)
    
    if image_path:
        try:
            client.sendLocalImage(
                imagePath=image_path,
                message=Message(text=text, mention=Mention(author_id, offset=len("🚦 "), length=len("@member"))),
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=800,
                ttl=30000
            )
        except:
            # Fallback nếu không gửi được ảnh
            client.replyMessage(
                Message(text=text, mention=Mention(author_id, offset=len("🚦 "), length=len("@member")), ttl=30000),
                message_object, thread_id, thread_type
            )
    else:
        client.replyMessage(
            Message(text=text, mention=Mention(author_id, offset=len("🚦 "), length=len("@member")), ttl=30000),
            message_object, thread_id, thread_type
        )

def show_admin_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh admin"""
    
    # Chỉ admin mới xem được
    if str(author_id) != str(ADMIN):
        client.replyMessage(
            Message(text="🚫 Chỉ admin mới có thể xem menu này!"),
            message_object, thread_id, thread_type
        )
        return
    
    text = f"""🔧 MENU ADMIN & QUẢN LÝ

👑 QUYỀN ADMIN:
   {PREFIX}admin on/off - Bật/tắt admin mode
   {PREFIX}notify on/off - Bật/tắt thông báo
   {PREFIX}stats - Xem thống kê chi tiết
   {PREFIX}clearstats - Xóa thống kê

🛠️ QUẢN LÝ BOT:
   {PREFIX}rs - Reset bot
   {PREFIX}kdl - Khởi tạo lại bot
   {PREFIX}advip - Thông tin admin
   {PREFIX}uptime - Thời gian chạy

📊 GIÁM SÁT:
   {PREFIX}ktra - Check ping độ trễ
   {PREFIX}auto_on - Bật auto thính
   {PREFIX}duyetmen - Duyệt men

🗑️ DỌN DẸP:
   {PREFIX}delall - Xóa tin nhắn
   {PREFIX}cap - Cap lại web

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_group_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh quản lý group"""
    
    text = f"""👥 MENU QUẢN LÝ GROUP

🏠 QUẢN LÝ THÀNH VIÊN:
   {PREFIX}tagall - Gọi tất cả thành viên
   {PREFIX}meid @user - Lấy ID thành viên
   {PREFIX}war - Lệnh war
   {PREFIX}reo - War tag

👮‍♂️ KIỂM SOÁT:
   {PREFIX}bot-group - Quản lý group
   {PREFIX}warpoll - Spam tạo bình chọn
   {PREFIX}chui1-52 - Spam chửi

🎭 TƯƠNG TÁC:
   {PREFIX}uptcard - Card cá nhân
   {PREFIX}bantho @user - Bàn thờ user

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_fun_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh giải trí"""
    
    text = f"""🎮 MENU GIẢI TRÍ & GAME

🎲 GAME & GIẢI TRÍ:
   {PREFIX}txiu - Game tài xỉu
   {PREFIX}tangai - Thả thính
   {PREFIX}boibai - Xem bói bài
   {PREFIX}meme - Ảnh meme funny

🎭 THẢ THÍNH & CHÚC MỪNG:
   {PREFIX}chuctet - Chúc tết
   {PREFIX}chucngungon - Chúc ngủ ngon  
   {PREFIX}chucvuive - Chúc vui vẻ

🌡️ THÔNG TIN:
   {PREFIX}thoitiet - Thông báo thời tiết

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_music_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh âm nhạc"""
    
    text = f"""🎵 MENU ÂM NHẠC & MEDIA

🎶 ÂM NHẠC:
   {PREFIX}nhac - Chọn và phát nhạc
   {PREFIX}voice - Tạo voice từ text

🎬 VIDEO GIẢI TRÍ:
   {PREFIX}chill - Video chill
   {PREFIX}animechill - Video anime chill
   {PREFIX}vdgirl - Video gái cute

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_media_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh ảnh/video"""
    
    text = f"""🖼️ MENU ẢNH & VIDEO

📸 ẢNH GIẢI TRÍ:
   {PREFIX}girl - Ảnh gái xinh
   {PREFIX}animegura - Ảnh anime
   {PREFIX}meme - Ảnh meme hài

🎨 TẠO ẢNH:
   {PREFIX}taoanh - Vẽ ảnh từ text
   {PREFIX}stk - Tạo sticker
   {PREFIX}media - Gửi ảnh từ link

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_nsfw_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu lệnh 18+"""
    
    text = f"""🔞 MENU CONTENT 18+

⚠️ CẢNH BÁO: Nội dung dành cho người trên 18 tuổi

🔞 VIDEO 18+:
   {PREFIX}vdsex - Video 18+
   {PREFIX}vd18 - Video người lớn
   {PREFIX}sexv4 - Video 18+ v4

📸 ẢNH 18+:
   {PREFIX}nude - Ảnh nude

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Sử dụng có trách nhiệm!
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_tools_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu công cụ tiện ích"""
    
    text = f"""🛠️ MENU CÔNG CỤ & TIỆN ÍCH

🔧 QR CODE:
   {PREFIX}qrcode - Tạo mã QR
   {PREFIX}scanqr - Scan mã QR

📞 LIÊN LẠC:
   {PREFIX}alo - Gọi bot
   {PREFIX}toadmin - Gửi tin nhắn cho admin

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_social_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu mạng xã hội"""
    
    text = f"""🌐 MENU MẠNG XÃ HỘI

📱 SPAM & TROLL:
   {PREFIX}spamsms - Spam SMS (cẩn thận!)

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Sử dụng có trách nhiệm, không làm tổn hại người khác!
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_ai_menu(message, message_object, thread_id, thread_type, author_id, client):
    """Menu chat AI"""
    
    text = f"""💬 MENU CHAT & AI

🤖 CHAT AI:
   {PREFIX}gpt - ChatGPT 5.0
   {PREFIX}bot - Gọi bot thông minh

💭 LỆNH NHANH (KHÔNG PREFIX):
   hello, hi, chào - Chào hỏi AI
   bot, bót - Gọi bot trả lời

━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Gõ {PREFIX}menu để về menu chính
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def get_mitaizl():
    return {
        'menu': show_main_menu,
        'menua': show_admin_menu,
        'menug': show_group_menu, 
        'menuf': show_fun_menu,
        'menum': show_music_menu,
        'menuv': show_media_menu,
        'menu18': show_nsfw_menu,
        'menut': show_tools_menu,
        'menus': show_social_menu,
        'menuc': show_ai_menu
    }