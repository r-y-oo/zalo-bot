import datetime
import pytz
import platform
import psutil
import os
from zlapi.models import Message, ThreadType
from config import ADMIN

def get_system_info():
    """Lấy thông tin hệ thống để hiển thị khi khởi động"""
    try:
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=True)
        
        # RAM info
        ram = psutil.virtual_memory()
        ram_used = ram.used / (1024 ** 3)
        ram_total = ram.total / (1024 ** 3)
        ram_percent = ram.percent
        
        # Disk info
        disk_path = '/' if platform.system() != "Windows" else 'C:\\'
        disk = psutil.disk_usage(disk_path)
        disk_free = disk.free / (1024 ** 3)
        disk_total = disk.total / (1024 ** 3)
        
        # OS info
        os_name = platform.system()
        os_version = platform.version()
        
        return {
            'cpu_percent': cpu_percent,
            'cpu_cores': cpu_cores,
            'ram_used': ram_used,
            'ram_total': ram_total,
            'ram_percent': ram_percent,
            'disk_free': disk_free,
            'disk_total': disk_total,
            'os_name': os_name,
            'os_version': os_version[:50] + '...' if len(os_version) > 50 else os_version
        }
    except Exception as e:
        print(f"Lỗi lấy thông tin hệ thống: {e}")
        return None

def get_bot_stats():
    """Lấy thống kê bot từ cache"""
    try:
        import json
        activity_file = 'modules/cache/user_activity.json'
        if os.path.exists(activity_file):
            with open(activity_file, 'r', encoding='utf-8') as f:
                activity_data = json.load(f)
            
            total_usage = sum(data.get('count', 1) for data in activity_data.values())
            unique_users = len(set(key.split('_')[0] for key in activity_data.keys() if '_' in key))
            
            return {
                'total_usage': total_usage,
                'unique_users': unique_users,
                'commands_tracked': len(activity_data)
            }
    except Exception as e:
        print(f"Lỗi lấy bot stats: {e}")
    
    return {'total_usage': 0, 'unique_users': 0, 'commands_tracked': 0}

def send_startup_notification(client):
    """Gửi thông báo khởi động đến admin"""
    try:
        # Lấy thời gian khởi động
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        startup_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        # Lấy thông tin hệ thống
        sys_info = get_system_info()
        bot_stats = get_bot_stats()
        
        # Đếm số modules đã load
        modules_count = count_loaded_modules()
        
        # Tạo thông báo khởi động
        startup_message = f"""
🚀 BOT KHỞI ĐỘNG THÀNH CÔNG 🚀

🕐 Thời gian: {startup_time}
🤖 Bot Name: {getattr(client, 'me_name', 'Bot by Duy Khanh')}
📱 Version: {getattr(client, 'version', '1.1')}
🆔 Bot ID: {client.uid}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 THÔNG TIN HỆ THỐNG:
"""
        
        if sys_info:
            startup_message += f"""
💻 OS: {sys_info['os_name']}
🔧 CPU: {sys_info['cpu_cores']} cores ({sys_info['cpu_percent']:.1f}%)
🧠 RAM: {sys_info['ram_used']:.1f}GB/{sys_info['ram_total']:.1f}GB ({sys_info['ram_percent']:.1f}%)
💾 Disk: {sys_info['disk_free']:.1f}GB free / {sys_info['disk_total']:.1f}GB total
"""
        else:
            startup_message += "\n❌ Không thể lấy thông tin hệ thống"
        
        startup_message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 THÔNG TIN MODULES:

📦 Modules loaded: {modules_count['total']}
🔄 Prefix commands: {modules_count['prefix']}
🚫 Noprefix commands: {modules_count['noprefix']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 THỐNG KÊ BOT:

📊 Tổng lượt sử dụng: {bot_stats['total_usage']}
👥 Users đã dùng: {bot_stats['unique_users']}
🔧 Commands tracked: {bot_stats['commands_tracked']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bot đã sẵn sàng nhận lệnh!

📝 Dùng -stats để xem thống kê chi tiết
🔔 Dùng -notify off để tắt thông báo
🆘 Dùng -toadmin để liên hệ admin
"""
        
        # Gửi thông báo đến admin với Message object
        client.sendMessage(
            Message(text=startup_message.strip()),
            ADMIN,
            ThreadType.USER
        )
        
        print(f"✅ Đã gửi thông báo khởi động đến admin: {ADMIN}")
        
        # Ghi log khởi động
        log_startup(startup_time)
        
    except Exception as e:
        print(f"❌ Lỗi gửi thông báo khởi động: {e}")

def count_loaded_modules():
    """Đếm số modules đã được load"""
    try:
        total = 0
        prefix = 0
        noprefix = 0
        
        # Đếm modules thường
        modules_path = 'modules'
        if os.path.exists(modules_path):
            prefix = len([f for f in os.listdir(modules_path) 
                         if f.endswith('.py') and f != '__init__.py'])
        
        # Đếm noprefix modules
        noprefix_path = 'modules/noprefix'
        if os.path.exists(noprefix_path):
            noprefix = len([f for f in os.listdir(noprefix_path) 
                           if f.endswith('.py') and f != '__init__.py'])
        
        total = prefix + noprefix
        
        return {
            'total': total,
            'prefix': prefix,
            'noprefix': noprefix
        }
    except Exception as e:
        print(f"Lỗi đếm modules: {e}")
        return {'total': 0, 'prefix': 0, 'noprefix': 0}

def log_startup(startup_time):
    """Ghi log thời gian khởi động"""
    try:
        log_file = 'modules/cache/startup_log.txt'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"Bot started at: {startup_time}\n")
            
    except Exception as e:
        print(f"Lỗi ghi log khởi động: {e}")

def send_shutdown_notification(client):
    """Gửi thông báo khi bot tắt"""
    try:
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        shutdown_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        # Lấy thống kê session
        bot_stats = get_bot_stats()
        
        shutdown_message = f"""
🛑 BOT ĐANG TẮT 🛑

🕐 Thời gian: {shutdown_time}
🤖 Bot ID: {client.uid}

📊 Thống kê session:
• Tổng lượt sử dụng: {bot_stats['total_usage']}
• Users hoạt động: {bot_stats['unique_users']}

✅ Session đã hoàn thành an toàn!
"""
        
        # Sử dụng Message object
        client.sendMessage(
            Message(text=shutdown_message.strip()),
            ADMIN,
            ThreadType.USER
        )
        
        print(f"✅ Đã gửi thông báo tắt bot đến admin")
        
    except Exception as e:
        print(f"❌ Lỗi gửi thông báo tắt bot: {e}")

def send_startup_error(error_message):
    """Gửi thông báo lỗi khởi động đến admin"""
    try:
        # Tạo một client tạm để gửi tin nhắn lỗi
        from zlapi import ZaloAPI
        from config import API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES
        
        temp_client = ZaloAPI(API_KEY, SECRET_KEY, imei=IMEI, session_cookies=SESSION_COOKIES)
        
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        error_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
        
        error_notification = f"""
🚨 LỖI KHỞI ĐỘNG BOT 🚨

🕐 Thời gian: {error_time}

❌ Lỗi:
{error_message}

🔧 Vui lòng kiểm tra và khắc phục!

📝 Có thể do:
• Mất kết nối internet
• API key/session cookies hết hạn
• Thiếu thư viện cần thiết
• Lỗi cấu hình
"""
        
        # Sử dụng Message object
        temp_client.sendMessage(
            Message(text=error_notification.strip()),
            ADMIN,
            ThreadType.USER
        )
        
        print(f"✅ Đã gửi thông báo lỗi đến admin")
        
    except Exception as e:
        print(f"❌ Không thể gửi thông báo lỗi: {e}")

def check_startup_issues(client):
    """Kiểm tra và báo cáo các vấn đề khi khởi động"""
    issues = []
    warnings = []
    
    try:
        # Kiểm tra folder cache
        if not os.path.exists('modules/cache'):
            issues.append("❌ Folder cache chưa tồn tại")
        
        # Kiểm tra noprefix modules
        if not os.path.exists('modules/noprefix'):
            warnings.append("⚠️ Folder noprefix không tồn tại")
        
        # Kiểm tra CommandHandler
        if not hasattr(client, 'command_handler'):
            issues.append("❌ CommandHandler không được khởi tạo")
        
        # Kiểm tra quyền ghi file
        test_file = 'modules/cache/test_write.tmp'
        try:
            os.makedirs('modules/cache', exist_ok=True)
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except:
            issues.append("❌ Không có quyền ghi file cache")
        
        # Kiểm tra dependencies
        missing_deps = check_dependencies()
        if missing_deps:
            warnings.extend([f"⚠️ Thiếu thư viện: {dep}" for dep in missing_deps])
        
        if issues or warnings:
            issue_message = "🔍 KIỂM TRA KHỞI ĐỘNG:\n\n"
            
            if issues:
                issue_message += "🚨 VẤN ĐỀ NGHIÊM TRỌNG:\n"
                issue_message += "\n".join(issues) + "\n\n"
            
            if warnings:
                issue_message += "⚠️ CẢNH BÁO:\n"
                issue_message += "\n".join(warnings) + "\n\n"
            
            issue_message += "🔧 Vui lòng kiểm tra và khắc phục!"
            
            # Sử dụng Message object
            client.sendMessage(
                Message(text=issue_message.strip()),
                ADMIN,
                ThreadType.USER
            )
            
    except Exception as e:
        print(f"Lỗi kiểm tra startup issues: {e}")

def check_dependencies():
    """Kiểm tra các thư viện cần thiết"""
    missing = []
    required_packages = [
        'psutil', 'pytz', 'colorama', 'pillow', 'pystyle'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

# Helper function để gọi từ bot.py
def notify_bot_startup(client):
    """Hàm chính để gọi từ bot.py"""
    print("🚀 Đang gửi thông báo khởi động...")
    send_startup_notification(client)
    check_startup_issues(client)