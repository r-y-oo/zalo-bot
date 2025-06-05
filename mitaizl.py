from zlapi.models import Message, ThreadType
import os
import importlib
import json
import datetime
import pytz
from config import PREFIX, ADMIN
import modules.bot_info
from modules.tagall import handle_tagall_command
import sys
from modules.menu import ping  
from modules.tagall import ft_vxkiue
sys.path.append('.')  # hoặc đường dẫn tuyệt đối đến thư mục chứa tagall.py
from modules.tagall import handle_tagall_command
from modules.menu import get_mitaizl  # Đúng tên file chứa menuzl
commands = get_mitaizl()

RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'

class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.mitaizl = self.load_mitaizl()
        self.auto_mitaizl = self.load_auto_mitaizl()
        self.adminon = self.load_admin_mode()  # Load trạng thái Admin Mode
        self.admin_notify_enabled = True  # Bật thông báo admin mặc định

    def load_admin_mode(self):
        """Đọc trạng thái Admin Mode từ file."""
        try:
            with open('modules/cache/admindata.json', 'r') as f:
                data = json.load(f)
                return data.get('adminon', False)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def save_admin_mode(self):
        """Lưu trạng thái Admin Mode vào file."""
        try:
            os.makedirs('modules/cache', exist_ok=True)
            with open('modules/cache/admindata.json', 'w') as f:
                json.dump({'adminon': self.adminon}, f)
        except Exception as e:
            print(f"Lỗi khi lưu admin mode: {e}")

    def load_mitaizl(self):
        mitaizl = {}
        from modules.tagall import ft_vxkiue
        mitaizl.update(ft_vxkiue())  # ← thêm dòng này

        from modules.sms import get_mitaizl
        mitaizl.update(get_mitaizl())
        
        modules_path = 'modules'
        for filename in os.listdir(modules_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{modules_path}.{module_name}')
                    if hasattr(module, 'get_mitaizl'):
                        mitaizl.update(module.get_mitaizl())
                except Exception as e:
                    print(f"{BOLD}{RED}Không thể load module: {module_name}. Lỗi: {e}{RESET}")
        return mitaizl

    def load_auto_mitaizl(self):
        """Load các lệnh không cần prefix từ folder 'modules/noprefix'."""
        auto_mitaizl = {}
        noprefix_modules_path = 'modules.noprefix'
        noprefix_folder = 'modules/noprefix'
        
        # Kiểm tra folder noprefix có tồn tại không
        if not os.path.exists(noprefix_folder):
            print(f"{BOLD}{RED}Folder {noprefix_folder} không tồn tại!{RESET}")
            return auto_mitaizl
            
        for filename in os.listdir(noprefix_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{noprefix_modules_path}.{module_name}')
                    if hasattr(module, 'get_mitaizl'):
                        noprefix_commands = module.get_mitaizl()
                        auto_mitaizl.update(noprefix_commands)
                        print(f"{BOLD}{GREEN}Da load module noprefix: {module_name} voi {len(noprefix_commands)} lenh{RESET}")
                except Exception as e:
                    print(f"{BOLD}{RED}Khong the load module noprefix: {module_name}. Loi: {e}{RESET}")
        
        print(f"{BOLD}{GREEN}Tong cong da load {len(auto_mitaizl)} lenh noprefix{RESET}")
        return auto_mitaizl

    def notify_admin_activity(self, message, author_id, thread_id, thread_type, command_type="command"):
        """Thông báo admin về hoạt động bot"""
        if not self.admin_notify_enabled:
            return
            
        # Không thông báo nếu chính admin sử dụng
        if str(author_id) == str(ADMIN):
            return
            
        # Kiểm tra có nên thông báo không (tránh spam)
        if not self.should_notify_admin(author_id, message):
            return
            
        try:
            # Lấy thông tin user
            user_name = self.get_user_name_safe(author_id)
            
            # Lấy thời gian hiện tại (Việt Nam)
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            current_time = datetime.datetime.now(vn_tz).strftime('%d/%m/%Y %H:%M:%S')
            
            # Tạo thông báo khác nhau cho group và chat riêng
            if thread_type == ThreadType.GROUP:
                group_name = self.get_group_name_safe(thread_id)
                notification_text = f"""
🤖 BOT ACTIVITY ALERT 🤖

👤 User: {user_name}
🆔 ID: {author_id}
💬 {command_type.title()}: "{message}"
📱 Trong Group: {group_name}
🕐 Thời gian: {current_time}

📍 Thread ID: {thread_id}
"""
            else:
                notification_text = f"""
🤖 BOT ACTIVITY ALERT 🤖

👤 User: {user_name}
🆔 ID: {author_id}
💬 {command_type.title()}: "{message}"
📱 Chat riêng
🕐 Thời gian: {current_time}

📍 Thread ID: {thread_id}
"""
            
            # Gửi thông báo đến admin với Message object
            self.client.sendMessage(
                Message(text=notification_text.strip()),
                ADMIN,
                ThreadType.USER
            )
            
            print(f"✅ Đã thông báo admin về hoạt động: {user_name} dùng '{message}'")
            
        except Exception as e:
            print(f"❌ Lỗi khi thông báo admin: {e}")

    def should_notify_admin(self, user_id, command):
        """Kiểm tra có nên thông báo admin không (tránh spam)"""
        try:
            activity_file = 'modules/cache/user_activity.json'
            activity_data = {}
            
            if os.path.exists(activity_file):
                with open(activity_file, 'r', encoding='utf-8') as f:
                    activity_data = json.load(f)
            
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
            
            # Lưu vào file
            os.makedirs(os.path.dirname(activity_file), exist_ok=True)
            with open(activity_file, 'w', encoding='utf-8') as f:
                json.dump(activity_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Lỗi kiểm tra thông báo admin: {e}")
            return False

    def get_user_name_safe(self, user_id):
        """Lấy tên user an toàn"""
        try:
            user_info = self.client.fetchUserInfo(user_id)
            if user_info and user_info.userInfo:
                return user_info.userInfo.get(user_id, {}).get('name', f'User_{user_id[-8:]}')
        except:
            pass
        return f'User_{user_id[-8:]}'

    def get_group_name_safe(self, thread_id):
        """Lấy tên group an toàn"""
        try:
            group_info = self.client.fetchGroupInfo(thread_id)
            if group_info and group_info.gridInfoMap:
                return group_info.gridInfoMap.get(thread_id, {}).name or f'Group_{thread_id[-8:]}'
        except:
            pass
        return f'Group_{thread_id[-8:]}'

    def handle_command(self, message, author_id, message_object, thread_id, thread_type):
        # Nếu lệnh là adminmode on/off thì bật/tắt Admin Mode
        if message.startswith(PREFIX + 'admin'):
            self.toggle_admin_mode(message, message_object, thread_id, thread_type, author_id)
            return
        
        # Kiểm tra lệnh auto (không cần prefix) TRƯỚC KHI kiểm tra admin mode
        auto_command_handler = self.auto_mitaizl.get(message.lower())
        if auto_command_handler:
            print(f"{BOLD}{GREEN}Thực thi lệnh noprefix: {message.lower()}{RESET}")
            
            # Thông báo admin về hoạt động noprefix
            self.notify_admin_activity(message, author_id, thread_id, thread_type, "noprefix command")
            
            auto_command_handler(message, message_object, thread_id, thread_type, author_id, self.client)
            return
        
        # Kiểm tra nếu Admin Mode đang bật và người gửi không phải admin thì bỏ qua
        if self.adminon and author_id not in ADMIN:
            return

        # Nếu không có prefix thì bỏ qua
        if not message.startswith(PREFIX):
            return

        # Xử lý lệnh chính
        command_name = message[len(PREFIX):].split(' ')[0].lower()
        command_handler = self.mitaizl.get(command_name)

        if command_handler:
            # Thông báo admin về hoạt động prefix command
            self.notify_admin_activity(message, author_id, thread_id, thread_type, "prefix command")
            
            command_handler(message, message_object, thread_id, thread_type, author_id, self.client)
        else:
            self.client.sendMessage(
                Message(text=f"Không tìm thấy lệnh '{command_name}'. Hãy dùng {PREFIX}menu để biết các lệnh có trên hệ thống."),
                thread_id, 
                thread_type
            )

    def toggle_admin_mode(self, message, message_object, thread_id, thread_type, author_id):
        """Bật/tắt Admin Mode với reply"""
        if author_id in ADMIN:
            if 'on' in message.lower():
                self.adminon = True
                self.save_admin_mode()
                self.client.replyMessage(
                    Message(text="🔓 Admin Đã Được Bật!"),
                    message_object, thread_id, thread_type
                )
            elif 'off' in message.lower():
                self.adminon = False
                self.save_admin_mode()
                self.client.replyMessage(
                    Message(text="🔓 Admin Đã Được Tắt!"),
                    message_object, thread_id, thread_type
                )
            else:
                self.client.replyMessage(
                    Message(text="🚦 Vui lòng chỉ định lệnh 'on' hoặc 'off'."),
                    message_object, thread_id, thread_type
                )
        else:
            self.client.replyMessage(
                Message(text="🚫 Tuổi Cặc Đòi Xài!"),
                message_object, thread_id, thread_type
            )
            
def is_wlgr(gr_id):
    wl_list = load_data(BOTSET_FILE)
    if "5" not in wl_list:
        wl_list["5"] = {}
    if "whitelist" not in wl_list["5"]:
        wl_list["5"]["whitelist"] = []
    ad_id = wl_list["5"]["whitelist"]
    gr_id = int(gr_id)
    return gr_id in ad_id

def add_wlgr(self,message_object,thread_id,thread_type,author_id):
    author_id = int(author_id)
    if not is_admin(str(author_id)):
        messages = "❌Bạn không phải là owner =))"
        self.replyMessage(
                Message(text=str(messages)),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
            )
        return
    if thread_type != ThreadType.GROUP:
        messages = "❌Vui lòng dùng trong nhóm"
        self.replyMessage(
                Message(text=str(messages)),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
            )
        return
    botset1 = load_data(BOTSET_FILE)
    thread_id=int(thread_id)
    if "5" not in botset1:
        botset1["5"] = {}
    if "whitelist" not in botset1["5"]:
        botset1["5"]["whitelist"] = []
    if thread_id in botset1["5"]["whitelist"]:  # Tránh thêm trùng lặp
        messages = "❌GR Đã được whitelist"
        self.replyMessage(
                Message(text=str(messages)),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
            )
        return
    if thread_id not in botset1["5"]["whitelist"]:  # Tránh thêm trùng lặp
        botset1["5"]["whitelist"].append(int(thread_id))
    save_data(BOTSET_FILE,botset1)
    gr = self.fetchGroupInfo(thread_id)
    gr_name = gr['gridInfoMap'][str(thread_id)].name
    length = len(str(gr_name))
    bold = MessageStyle(style="bold", length=length, offset=10,auto_format=False)
    style = MultiMsgStyle([bold])
    messages = f"✔ Đã thêm {gr_name} vào danh sách group whitelist"
    self.replyMessage(
            Message(text=str(messages),style=style),
            message_object,
            thread_id=thread_id,
            thread_type=thread_type,
        )
    return

def rm_wlgr(self,message_object,thread_id,thread_type,author_id):
    author_id = int(author_id)
    if not is_admin(str(author_id)):
        messages = "❌Bạn không phải là owner =))"
        self.replyMessage(
                Message(text=str(messages)),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
            )
        return
    if thread_type != ThreadType.GROUP:
        messages = "❌Vui lòng dùng trong nhóm"
        self.replyMessage(
                Message(text=str(messages)),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
            )
        return
    botset1 = load_data(BOTSET_FILE)
    if "5" not in botset1:
        botset1["5"] = {}
    if "whitelist" not in botset1["5"]:
        botset1["5"]["whitelist"] = []
    if int(thread_id) in botset1["5"]["whitelist"]:  # Tránh thêm trùng lặp
        botset1["5"]["whitelist"].remove(int(thread_id))
    save_data(BOTSET_FILE,botset1)
    gr = self.fetchGroupInfo(thread_id)
    gr_name = gr['gridInfoMap'][str(thread_id)].name
    length = len(str(gr_name))
    bold = MessageStyle(style="bold", length=length, offset=10,auto_format=False)
    messages = f"✔ Đã xoá {gr_name} vào danh sách group whitelist"
    style = MultiMsgStyle([bold])
    self.replyMessage(
            Message(text=str(messages),style=style),
            message_object,
            thread_id=thread_id,
            thread_type=thread_type,
        )
    return

def is_admin(author_id):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    if author_id in admin_bot:
        return True
    else:
        return False

def handle_bot_admin(bot):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    if bot.uid not in admin_bot:
        admin_bot.append(bot.uid)
        settings['admin_bot'] = admin_bot
        write_settings(settings)
        print(f"Đã thêm 👑{get_user_name_by_id(bot, bot.uid)} 🆔 {bot.uid} cho lần đầu tiên khởi động vào danh sách Admin 🤖BOT ✅")


def get_allowed_thread_ids():
    """Lấy danh sách các thread ID được phép từ setting.json."""
    settings = read_settings()
    return settings.get('allowed_thread_ids', [])

def bot_on_group(bot, thread_id):
    """Thêm thread_id vào danh sách được phép."""
    try:
        settings = read_settings()
        allowed_thread_ids = settings.get('allowed_thread_ids', [])
        group = bot.fetchGroupInfo(thread_id).gridInfoMap[thread_id]

        if thread_id not in allowed_thread_ids:
            allowed_thread_ids.append(thread_id)
            settings['allowed_thread_ids'] = allowed_thread_ids
            write_settings(settings)

            return f"🤖BOT đã được bật trong Group: {group.name}\n"
    except Exception as e:
        print(f"Error: {e}")
        return "Đã xảy ra lỗi gì đó🤧"

def bot_off_group(bot, thread_id):
    """Loại bỏ thread_id khỏi danh sách được phép."""
    try:
        settings = read_settings()
        allowed_thread_ids = settings.get('allowed_thread_ids', [])
        group = bot.fetchGroupInfo(thread_id).gridInfoMap[thread_id]

        if thread_id in allowed_thread_ids:
            allowed_thread_ids.remove(thread_id)
            settings['allowed_thread_ids'] = allowed_thread_ids
            write_settings(settings)

            return f"🤖BOT đã được tắt trong Group: {group.name}\n"
    except Exception as e:
        print(f"Error: {e}")