import json
import os
import datetime
import pytz
from zlapi.models import Message, MessageStyle
from config import ADMIN, PREFIX

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài", 
    'description': "Quản lý thông báo admin và xem thống kê hoạt động"
}

def toggle_admin_notify(message, message_object, thread_id, thread_type, author_id, client):
    """Bật/tắt thông báo admin"""
    if str(author_id) != str(ADMIN):
        client.replyMessage(
            Message(text="🚫 Chỉ admin mới có thể sử dụng lệnh này!", ttl=30000),
            message_object, thread_id, thread_type
        )
        return
    
    parts = message.split()
    if len(parts) < 2:
        client.replyMessage(
            Message(text="📝 Sử dụng: -notify on/off", ttl=30000),
            message_object, thread_id, thread_type
        )
        return
    
    action = parts[1].lower()
    
    try:
        # Load current settings
        settings_file = 'modules/cache/admin_settings.json'
        settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        
        if action == 'on':
            settings['admin_notify_enabled'] = True
            status_text = "✅ Đã BẬT thông báo admin!"
        elif action == 'off':
            settings['admin_notify_enabled'] = False
            status_text = "❌ Đã TẮT thông báo admin!"
        else:
            client.replyMessage(
                Message(text="❌ Chỉ dùng 'on' hoặc 'off'!", ttl=30000),
                message_object, thread_id, thread_type
            )
            return
        
        # Save settings
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        client.replyMessage(
            Message(text=status_text, ttl=30000),
            message_object, thread_id, thread_type
        )
        
    except Exception as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi: {str(e)}", ttl=30000),
            message_object, thread_id, thread_type
        )

def show_bot_stats(message, message_object, thread_id, thread_type, author_id, client):
    """Hiển thị thống kê hoạt động bot"""
    if str(author_id) != str(ADMIN):
        client.replyMessage(
            Message(text="🚫 Chỉ admin mới có thể xem thống kê!", ttl=30000),
            message_object, thread_id, thread_type
        )
        return
    
    try:
        activity_file = 'modules/cache/user_activity.json'
        if not os.path.exists(activity_file):
            client.replyMessage(
                Message(text="📊 Chưa có dữ liệu hoạt động nào!", ttl=30000),
                message_object, thread_id, thread_type
            )
            return
        
        with open(activity_file, 'r', encoding='utf-8') as f:
            activity_data = json.load(f)
        
        if not activity_data:
            client.replyMessage(
                Message(text="📊 Chưa có dữ liệu hoạt động nào!", ttl=30000),
                message_object, thread_id, thread_type
            )
            return
        
        # Phân tích dữ liệu
        user_stats = {}
        command_stats = {}
        total_usage = 0
        
        for user_command, data in activity_data.items():
            if '_' in user_command:
                user_id, command = user_command.rsplit('_', 1)
                count = data.get('count', 1)
                total_usage += count
                
                # Thống kê theo user
                if user_id not in user_stats:
                    user_stats[user_id] = 0
                user_stats[user_id] += count
                
                # Thống kê theo command
                if command not in command_stats:
                    command_stats[command] = 0
                command_stats[command] += count
        
        # Tạo báo cáo
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        # Top 5 users
        top_users = sorted(user_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top 5 commands
        top_commands = sorted(command_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        stats_text = f"""
📊 THỐNG KÊ HOẠT ĐỘNG BOT 📊

🕐 Thời gian: {current_time}
📈 Tổng lượt sử dụng: {total_usage}
👥 Số users đã dùng: {len(user_stats)}
🔧 Số commands được dùng: {len(command_stats)}

🏆 TOP 5 USERS HOẠT ĐỘNG:
"""
        
        for i, (user_id, count) in enumerate(top_users, 1):
            user_display = f"User_{user_id[-8:]}"
            try:
                # Thử lấy tên user thật
                user_info = client.fetchUserInfo(user_id)
                if user_info and user_info.userInfo:
                    user_name = user_info.userInfo.get(user_id, {}).get('name', user_display)
                    user_display = user_name
            except:
                pass
            
            stats_text += f"{i}. {user_display}: {count} lượt\n"
        
        stats_text += f"""
🔥 TOP 5 COMMANDS PHỔ BIẾN:
"""
        
        for i, (command, count) in enumerate(top_commands, 1):
            stats_text += f"{i}. '{command}': {count} lượt\n"
        
        stats_text += "\n📝 Dùng -clearstats để xóa thống kê"
        
        # Tạo style cho text
        font_style = MessageStyle(
            style="font",
            size="12",
            offset=0,
            length=len(stats_text),
            auto_format=False
        )
        
        client.replyMessage(
            Message(text=stats_text.strip(), style=font_style, ttl=30000),
            message_object, thread_id, thread_type
        )
        
    except Exception as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi khi tạo thống kê: {str(e)}", ttl=30000),
            message_object, thread_id, thread_type
        )

def clear_bot_stats(message, message_object, thread_id, thread_type, author_id, client):
    """Xóa thống kê hoạt động"""
    if str(author_id) != str(ADMIN):
        client.replyMessage(
            Message(text="🚫 Chỉ admin mới có thể xóa thống kê!", ttl=30000),
            message_object, thread_id, thread_type
        )
        return
    
    try:
        activity_file = 'modules/cache/user_activity.json'
        if os.path.exists(activity_file):
            os.remove(activity_file)
            client.replyMessage(
                Message(text="🗑️ Đã xóa toàn bộ thống kê hoạt động!", ttl=30000),
                message_object, thread_id, thread_type
            )
        else:
            client.replyMessage(
                Message(text="📊 Không có dữ liệu nào để xóa!", ttl=30000),
                message_object, thread_id, thread_type
            )
    except Exception as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi khi xóa thống kê: {str(e)}", ttl=30000),
            message_object, thread_id, thread_type
        )

def send_message_to_admin(message, message_object, thread_id, thread_type, author_id, client):
    """Gửi tin nhắn đến admin (dành cho users)"""
    # Lấy nội dung tin nhắn
    parts = message.split(' ', 1)
    if len(parts) < 2:
        client.replyMessage(
            Message(text="📝 Sử dụng: -toadmin [nội dung tin nhắn]", ttl=30000),
            message_object, thread_id, thread_type
        )
        return
    
    user_message = parts[1]
    
    try:
        # Lấy thông tin user
        user_name = f"User_{author_id[-8:]}"
        try:
            user_info = client.fetchUserInfo(author_id)
            if user_info and user_info.userInfo:
                user_name = user_info.userInfo.get(author_id, {}).get('name', user_name)
        except:
            pass
        
        # Lấy thời gian
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        # Tạo tin nhắn gửi đến admin
        admin_message = f"""
📨 TIN NHẮN TỪ USER 📨

👤 From: {user_name}
🆔 ID: {author_id}
🕐 Thời gian: {current_time}

💬 Nội dung:
{user_message}

📍 Thread ID: {thread_id}
"""
        
        # Gửi đến admin
        from zlapi.models import ThreadType
        client.sendMessage(
            Message(text=admin_message.strip()),
            ADMIN,
            ThreadType.USER
        )
        
        # Xác nhận với user
        client.replyMessage(
            Message(text="✅ Đã gửi tin nhắn đến admin thành công!", ttl=30000),
            message_object, thread_id, thread_type
        )
        
    except Exception as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi khi gửi tin nhắn: {str(e)}", ttl=30000),
            message_object, thread_id, thread_type
        )

def get_mitaizl():
    return {
        'notify': toggle_admin_notify,
        'stats': show_bot_stats,
        'clearstats': clear_bot_stats,
        'toadmin': send_message_to_admin
    }