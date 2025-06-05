from zlapi.models import Message, Mention
from config import PREFIX

def show_help_guide(message, message_object, thread_id, thread_type, author_id, client):
    """Hướng dẫn sử dụng bot"""
    
    text = f"""📖 HƯỚNG DẪN SỬ DỤNG BOT

🚀 CÁCH BẮT ĐẦU:
   1. Gõ {PREFIX}menu - Xem menu chính
   2. Chọn danh mục muốn xem
   3. Sử dụng lệnh theo hướng dẫn

📂 CÁC DANH MỤC CHÍNH:

🔧 {PREFIX}menua - Lệnh admin (chỉ admin)
👥 {PREFIX}menug - Quản lý group  
🎮 {PREFIX}menuf - Giải trí & game
🎵 {PREFIX}menum - Âm nhạc & media
🖼️ {PREFIX}menuv - Ảnh & video
🔞 {PREFIX}menu18 - Content 18+
🛠️ {PREFIX}menut - Công cụ tiện ích
🌐 {PREFIX}menus - Mạng xã hội
💬 {PREFIX}menuc - Chat AI
📊 {PREFIX}stats - Thống kê (admin)

💡 LỆNH NHANH (KHÔNG CẦN PREFIX):
   • hello, hi, chào - Chào bot
   • bot, bót - Gọi bot
   • system - Thông tin hệ thống

🎯 VÍ DỤ SỬ DỤNG:
   • {PREFIX}menu → Xem menu chính
   • {PREFIX}menug → Xem lệnh group
   • {PREFIX}girl → Xem ảnh gái
   • hello → Chào bot (không cần -)

📞 HỖ TRỢ:
   • {PREFIX}toadmin [tin nhắn] - Liên hệ admin
   • {PREFIX}help - Xem hướng dẫn này

━━━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 Bot by Duy Khanh | v2.1.0
🎯 Prefix hiện tại: {PREFIX}
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_prefix_info(message, message_object, thread_id, thread_type, author_id, client):
    """Thông tin về prefix"""
    
    text = f"""ℹ️ THÔNG TIN PREFIX

🔤 PREFIX HIỆN TẠI: {PREFIX}

📝 CÁCH SỬ DỤNG PREFIX:
   • Lệnh có prefix: {PREFIX}menu, {PREFIX}girl, {PREFIX}gpt
   • Lệnh không prefix: hello, hi, bot, system

💡 VÍ DỤ:
   ✅ Đúng: {PREFIX}menu
   ❌ Sai: menu (thiếu prefix)
   
   ✅ Đúng: hello
   ❌ Sai: {PREFIX}hello (thừa prefix)

🎯 Gõ {PREFIX}help để xem hướng dẫn đầy đủ
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_commands_list(message, message_object, thread_id, thread_type, author_id, client):
    """Danh sách tất cả lệnh (tóm tắt)"""
    
    text = f"""📋 DANH SÁCH LỆNH TÓM TẮT

🔧 ADMIN: {PREFIX}admin, {PREFIX}stats, {PREFIX}notify
👥 GROUP: {PREFIX}tagall, {PREFIX}war, {PREFIX}meid
🎮 GAME: {PREFIX}txiu, {PREFIX}tangai, {PREFIX}boibai
🎵 MEDIA: {PREFIX}nhac, {PREFIX}voice, {PREFIX}chill
🖼️ ẢNH: {PREFIX}girl, {PREFIX}meme, {PREFIX}taoanh
🔞 18+: {PREFIX}vdsex, {PREFIX}nude (18+)
🛠️ TOOLS: {PREFIX}qrcode, {PREFIX}toadmin
🌐 SOCIAL: {PREFIX}spamsms
💬 AI: {PREFIX}gpt, hello, hi, bot

📱 Chi tiết: {PREFIX}menu → chọn danh mục
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def show_noprefix_commands(message, message_object, thread_id, thread_type, author_id, client):
    """Hướng dẫn lệnh không prefix"""
    
    text = f"""🚫 LỆNH KHÔNG CẦN PREFIX

💬 CHAT & CHÀO HỎI:
   • hello - Chào bot
   • hi - Chào bot
   • chào - Chào bot (tiếng Việt)

🤖 GỌI BOT:
   • bot - Gọi bot trả lời
   • bót - Gọi bot trả lời

💻 THÔNG TIN HỆ THỐNG:
   • system - Xem thông tin hệ thống

✨ ĐẶC BIỆT:
   Các lệnh này KHÔNG CẦN prefix {PREFIX}
   Chỉ cần gõ trực tiếp!

💡 VÍ DỤ:
   Gõ: hello
   Bot sẽ trả lời: Xin chào! 👋

🎯 Các lệnh khác cần prefix {PREFIX}
   Gõ {PREFIX}menu để xem menu đầy đủ
"""
    
    client.replyMessage(
        Message(text=text),
        message_object, thread_id, thread_type
    )

def get_mitaizl():
    return {
        'help': show_help_guide,
        'prefixinfo': show_prefix_info,
        'commands': show_commands_list,
        'noprefix': show_noprefix_commands
    }