import datetime
import pytz
from zlapi.models import Message, ThreadType
from config import ADMIN
import json
import os

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "Thông báo admin khi có người dùng bot"
}

def get_user_info_cache_file():
    """Đường dẫn file cache thông tin user"""
    return 'modules/cache/user_activity.json'

def load_user_activity():
    """Load thông tin hoạt động user từ cache"""
    try:
        cache_file = get_user_info_cache_file()
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Lỗi load user activity: {e}")
    return {}

def save_user_activity(data):
    """Lưu thông tin hoạt động user vào cache"""
    try:
        cache_file = get_user_info_cache_file()
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi save user activity: {e}")

def get_user_name_safe(client, user_id):
    """Lấy tên user an toàn"""
    try:
        user_info = client.fetchUserInfo(user_id)
        if user_info and user_info.userInfo:
            return user_info.userInfo.get(user_id, {}).get('name', f'User_{user_id[-8:]}')
    except:
        pass
    return f'User_{user_id[-8:]}'

def get_group_name_safe(client, thread_id):
    """Lấy tên group an toàn"""
    try:
        group_info = client.fetchGroupInfo(thread_id)
        if group_info and group_info.gridInfoMap:
            return group_info.gridInfoMap.get(thread_id, {}).name or f'Group_{thread_id[-8:]}'
    except:
        pass
    return f'Group_{thread_id[-8:]}'

def should_notify_admin(user_id, command):
    """Kiểm tra có nên thông báo admin không (tránh spam)"""
    activity_data = load_user_activity()
    
    current_time = datetime.datetime.now()
    user_key = f"{user_id}_{command}"
    
    # Kiểm tra lần cuối thông báo
    if user_key in activity_data:
        last_notify = datetime.datetime.fromisoformat(activity_data[user_key]['last_notify'])
        # Chỉ thông báo nếu đã quá 30 phút
        if (current_time - last_notify).total_seconds() < 1800:  # 30 phút
            return False
    
    # Cập nhật thời gian thông báo
    activity_data[user_key] = {
        'last_notify': current_time.isoformat(),
        'count': activity_data.get(user_key, {}).get('count', 0) + 1
    }
    
    save_user_activity(activity_data)
    return True

def notify_admin_usage(message, message_object, thread_id, thread_type, author_id, client):
    """Hàm chính để thông báo admin"""
    
    # Không thông báo nếu chính admin sử dụng
    if str(author_id) == str(ADMIN):
        return
    
    # Chỉ thông báo cho một số commands quan trọng
    important_commands = ['system', 'admin', 'bot', 'hi', 'hello']
    command_used = message.lower().strip()
    
    if command_used not in important_commands:
        return
    
    # Kiểm tra có nên thông báo không (tránh spam)
    if not should_notify_admin(author_id, command_used):
        return
    
    try:
        # Lấy thông tin user và group
        user_name = get_user_name_safe(client, author_id)
        
        # Lấy thời gian hiện tại (Việt Nam)
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        # Tạo thông báo khác nhau cho group và chat riêng
        if thread_type == ThreadType.GROUP:
            group_name = get_group_name_safe(client, thread_id)
            notification_text = f"""
🤖 BOT ACTIVITY ALERT 🤖

👤 User: {user_name}
🆔 ID: {author_id}
💬 Command: "{command_used}"
📱 Trong Group: {group_name}
🕐 Thời gian: {current_time}

📍 Thread ID: {thread_id}
"""
        else:
            notification_text = f"""
🤖 BOT ACTIVITY ALERT 🤖

👤 User: {user_name}
🆔 ID: {author_id}
💬 Command: "{command_used}"
📱 Chat riêng
🕐 Thời gian: {current_time}

📍 Thread ID: {thread_id}
"""
        
        # Gửi thông báo đến admin
        client.sendMessage(
            notification_text.strip(),
            ADMIN,
            ThreadType.USER
        )
        
        print(f"✅ Đã thông báo admin về hoạt động: {user_name} dùng '{command_used}'")
        
    except Exception as e:
        print(f"❌ Lỗi khi thông báo admin: {e}")

def get_mitaizl():
    """
    Trả về dict các commands sẽ trigger thông báo admin
    Chỉ monitor một số commands quan trọng
    """
    return {
        'system': notify_admin_usage,
        'admin': notify_admin_usage,
    }