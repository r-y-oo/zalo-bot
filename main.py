import os
import sys
import time
import json
import random
import threading
import subprocess
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from colorama import Fore, Style, init
# from menu2 import get_mitaizl
from config import API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import Message, MultiMsgStyle, MessageStyle, ThreadType
from mitaizl import CommandHandler
from utils.logging_utils import Logging
from modules.noprefix.eventgroup import handle_event
from modules.bot_info import handle_bot_admin, get_user_name_by_id

# Khởi tạo màu terminal
init(autoreset=True)

logger = Logging()
uid = "397889269472130850"

# Màu in ra terminal
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]
colors1 = [
    "FF9900", "FFFF33", "33FFFF", "FF99FF", "FF3366", "FFFF66", "FF00FF", "66FF99", "00CCFF",
    "FF0099", "FF0066", "0033FF", "FF9999", "00FF66", "00FFFF", "CCFFFF", "8F00FF", "FF00CC",
    "FF0000", "FF1100", "FF3300", "FF4400", "FF5500", "FF6600", "FF7700", "FF8800", "FF9900",
    "FFaa00", "FFbb00", "FFcc00", "FFdd00", "FFee00", "FFff00", "FFFFFF", "FFEBCD", "F5F5DC",
    "F0FFF0", "F5FFFA", "F0FFFF", "F0F8FF", "FFF5EE", "F5F5F5"
]

temp_thread_storage = {}

def hex_to_ansi(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'


class ResetBot:
    def __init__(self, reset_interval=38800):
        self.reset_event = threading.Event()
        self.reset_interval = reset_interval
        self.load_autorestart_setting()

    def load_autorestart_setting(self):
        try:
            with open("seting.json", "r") as f:
                settings = json.load(f)
                self.autorestart = settings.get("autorestart", "False") == "True"

            if self.autorestart:
                logger.info("Chế độ auto restart đang được bật")
                threading.Thread(target=self.reset_code_periodically, daemon=True).start()
            else:
                logger.warning("Chế độ auto restart đang bị tắt")
        except Exception as e:
            logger.error(f"Lỗi khi tải cấu hình autorestart: {e}")
            self.autorestart = False

    def reset_code_periodically(self):
        while not self.reset_event.is_set():
            time.sleep(self.reset_interval)
            logger.restart("Đang tiến hành khởi động lại bot...")
            self.restart_bot()

    def restart_bot(self):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            logger.info(f"Bot khởi động lại thành công vào lúc: {current_time}")
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as e:
            logger.error(f"Lỗi khi khởi động lại bot: {e}")


class Client(ZaloAPI):
    subprocess.Popen(['python', 'utils/clearCPU.py'])

    def __init__(self, api_key, secret_key, imei, session_cookies, reset_interval=7200):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.command_handler = CommandHandler(self)
        self.reset_bot = ResetBot(reset_interval)
        self.group_info_cache = {}
        self.last_sms_times = {}
        self.session = requests.Session()

        retry_strategy = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        logger.logger('EVENT GROUP', 'Đang lắng nghe sự kiện nhóm...')

    def onLoggedIn(self, phone=None):
        self.uid = self._state.user_id
        logger.info(f"Đăng nhập thành công với uid: {self.uid}")
        try:
            handle_bot_admin(self)
            logger.success(f"Thêm ADMIN BOT thành công: {get_user_name_by_id(self, self.uid)} 🆔 {self.uid}")
        except Exception as e:
            logger.error(f"Lỗi khi thêm admin: {e}")

    def onEvent(self, event_data, event_type):
        handle_event(self, event_data, event_type)
        threading.Thread(target=self.handle_event, args=(event_data, event_type), daemon=True).start()

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        try:
            message_text = message.text if isinstance(message, Message) else str(message)
            self.command_handler.handle_command(message_text, author_id, message_object, thread_id, thread_type)

            author_info = self.fetchUserInfo(author_id).changed_profiles.get(author_id, {})
            author_name = author_info.get('zaloName', 'Không xác định')

            group_info = self.fetchGroupInfo(thread_id)
            group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', 'Không xác định')

            current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
            colors_selected = random.sample(colors1, 9)

            output = (
                f"{hex_to_ansi(colors_selected[0])}{Style.BRIGHT}------------------------------{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[1])}• Message: {message_text}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[2])}• Message ID: {mid}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[3])}• ID NGƯỜI DÙNG: {author_id}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[4])}• TÊN NGƯỜI DÙNG: {author_name}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[5])}• ID NHÓM: {thread_id}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[6])}• TÊN NHÓM: {group_name}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[7])}• TYPE: {thread_type}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[8])}• THỜI GIAN: {current_time}{Style.RESET_ALL}\n"
                f"{hex_to_ansi(colors_selected[0])}{Style.BRIGHT}------------------------------{Style.RESET_ALL}"
            )
            print(output)

            # Gửi tin nhắn auto-reply nếu là chat riêng
            if author_id != uid and thread_type == ThreadType.USER:
                now = time.time()
                if author_id in temp_thread_storage and now - temp_thread_storage[author_id] < 7200:
                    return

                msg = f"Chào {author_name} 𝘼𝙣𝙩𝙞 𝙈𝙞𝙣𝙞 Đang Bận Bạn Nhắn Lại Sau Nhé 🐰"
                styles = MultiMsgStyle([
                    MessageStyle(offset=0, length=2, style="color", color="#a24ffb", auto_format=False),
                    MessageStyle(offset=2, length=len(msg)-2, style="color", color="#ffaf00", auto_format=False),
                    MessageStyle(offset=0, length=len(msg), style="font", size="3", auto_format=False),
                    MessageStyle(offset=0, length=len(msg), style="bold", auto_format=False),
                    MessageStyle(offset=0, length=len(msg), style="italic", auto_format=False)
                ])
                self.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type)
                temp_thread_storage[author_id] = now

        except Exception as e:
            logger.error(f"Lỗi xử lý tin nhắn: {e}")


if __name__ == "__main__":
    try:
        client = Client(API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES)
        client.listen(thread=True, delay=0)
    except Exception as e:
        logger.error(f"Không thể đăng nhập bot: {e}")