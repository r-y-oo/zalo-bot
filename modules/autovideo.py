from zlapi.models import Message
import requests
import threading
import time
import datetime
from config import ADMIN

des = {
    'version': "1.0.0",
    'credits': "時崎狂三 ",
    'description': "Gửi video tự động theo giờ"
}

# Biến lưu trạng thái auto video
auto_video_status = {}
auto_video_threads = {}

def get_video_url():
    """Lấy link video từ API giống videogai5.py"""
    api_url = 'https://api.sumiproject.net/video/videogai'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data.get('url', '')
        
    except Exception as e:
        print(f"Lỗi khi lấy video: {str(e)}")
        return None

def send_auto_video(client, thread_id, thread_type, interval_minutes):
    """Gửi video tự động theo khoảng thời gian"""
    while auto_video_status.get(thread_id, False):
        try:
            video_url = get_video_url()
            if video_url:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                message_text = f"🎬 Video tự động lúc {current_time}"
                message_to_send = Message(text=message_text)
                
                thumbnail_url = 'https://imgur.com/a/CHKogcV'
                duration = '100'
                
                client.sendRemoteVideo(
                    video_url,
                    thumbnail_url,
                    duration=duration,
                    message=message_to_send,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1080,
                    height=1920
                )
                
            # Chờ theo khoảng thời gian đã định (tính bằng phút)
            time.sleep(interval_minutes * 60)
            
        except Exception as e:
            print(f"Lỗi trong auto video: {str(e)}")
            time.sleep(60)  # Chờ 1 phút trước khi thử lại

def handle_autovideo_start(message, message_object, thread_id, thread_type, author_id, client):
    """Bắt đầu auto video"""
    # Kiểm tra quyền admin
    if str(author_id) != ADMIN:
        error_message = Message(text="❌ Chỉ admin mới có thể sử dụng lệnh này!")
        client.sendMessage(error_message, thread_id, thread_type)
        return
    
    try:
        # Lấy thời gian interval từ tin nhắn (mặc định 60 phút)
        parts = message.split()
        interval_minutes = 10  # Mặc định 60 phút
        
        if len(parts) > 1:
            try:
                interval_minutes = int(parts[1])
                if interval_minutes < 1:
                    interval_minutes = 0
            except ValueError:
                interval_minutes = 10
        
        # Kiểm tra xem đã có auto video chưa
        if auto_video_status.get(thread_id, False):
            message_reply = Message(text="⚠️ Auto video đã đang chạy trong nhóm này!")
        else:
            # Bắt đầu auto video
            auto_video_status[thread_id] = True
            
            # Tạo thread mới để chạy auto video
            video_thread = threading.Thread(
                target=send_auto_video,
                args=(client, thread_id, thread_type, interval_minutes),
                daemon=True
            )
            auto_video_threads[thread_id] = video_thread
            video_thread.start()
            
            message_reply = Message(text=f"✅ Đã bật auto video!\n⏰ Gửi video mỗi {interval_minutes} phút\n📝 Dùng 'autovideo stop' để tắt")
        
        client.sendMessage(message_reply, thread_id, thread_type)
        
    except Exception as e:
        error_message = Message(text=f"❌ Lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def handle_autovideo_stop(message, message_object, thread_id, thread_type, author_id, client):
    """Dừng auto video"""
    # Kiểm tra quyền admin
    if str(author_id) != ADMIN:
        error_message = Message(text="❌ Chỉ admin mới có thể sử dụng lệnh này!")
        client.sendMessage(error_message, thread_id, thread_type)
        return
    
    try:
        if auto_video_status.get(thread_id, False):
            # Dừng auto video
            auto_video_status[thread_id] = False
            
            # Xóa thread khỏi dict
            if thread_id in auto_video_threads:
                del auto_video_threads[thread_id]
            
            message_reply = Message(text="⏹️ Đã tắt auto video!")
        else:
            message_reply = Message(text="⚠️ Auto video không đang chạy trong nhóm này!")
        
        client.sendMessage(message_reply, thread_id, thread_type)
        
    except Exception as e:
        error_message = Message(text=f"❌ Lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def handle_autovideo_status(message, message_object, thread_id, thread_type, author_id, client):
    """Kiểm tra trạng thái auto video"""
    try:
        if auto_video_status.get(thread_id, False):
            status_text = "🟢 Auto video đang chạy"
        else:
            status_text = "🔴 Auto video đang tắt"
        
        # Đếm số nhóm đang chạy auto video
        active_groups = sum(1 for status in auto_video_status.values() if status)
        
        message_reply = Message(text=f"📊 Trạng thái Auto Video:\n{status_text}\n\n📈 Tổng nhóm đang chạy: {active_groups}")
        client.sendMessage(message_reply, thread_id, thread_type)
        
    except Exception as e:
        error_message = Message(text=f"❌ Lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def handle_autovideo_help(message, message_object, thread_id, thread_type, author_id, client):
    """Hiển thị hướng dẫn sử dụng"""
    help_text = """🎬 HƯỚNG DẪN AUTO VIDEO

📝 Các lệnh:
• autovideo start [phút] - Bật auto video
• autovideo stop - Tắt auto video  
• autovideo status - Xem trạng thái
• autovideo help - Xem hướng dẫn

⏰ Ví dụ:
• autovideo start - Gửi video mỗi 60 phút
• autovideo start 30 - Gửi video mỗi 30 phút
• autovideo start 120 - Gửi video mỗi 2 giờ

⚠️ Chỉ admin mới có thể sử dụng"""
    
    message_reply = Message(text=help_text)
    client.sendMessage(message_reply, thread_id, thread_type)

def handle_autovideo_command(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh auto video chính"""
    parts = message.lower().split()
    
    if len(parts) < 2:
        handle_autovideo_help(message, message_object, thread_id, thread_type, author_id, client)
        return
    
    subcommand = parts[1]
    
    if subcommand == "start":
        handle_autovideo_start(message, message_object, thread_id, thread_type, author_id, client)
    elif subcommand == "stop":
        handle_autovideo_stop(message, message_object, thread_id, thread_type, author_id, client)
    elif subcommand == "status":
        handle_autovideo_status(message, message_object, thread_id, thread_type, author_id, client)
    elif subcommand == "help":
        handle_autovideo_help(message, message_object, thread_id, thread_type, author_id, client)
    else:
        handle_autovideo_help(message, message_object, thread_id, thread_type, author_id, client)

def get_mitaizl():
    return {
        'autovideo': handle_autovideo_command
    }