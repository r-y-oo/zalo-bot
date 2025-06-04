from config import API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES,PREFIX
from mitaizl import CommandHandler
from zlapi import ZaloAPI
from zlapi.models import Message
from modules.bot_info import *
from modules.welcome import welcome
from modules.startup_notify import notify_bot_startup
from colorama import Fore, Style, init
from modules.menu import get_mitaizl  # Đảm bảo đúng tên file chứa menuzl
import threading
import time
commands = get_mitaizl()


init(autoreset=True)

class Client(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        handle_bot_admin(self)
        self.version = 1.1
        self.me_name = "Bot by Duy Khanh"
        self.date_update = "26/9/2024"
        self.command_handler = CommandHandler(self)
        
        # Gửi thông báo khởi động sau khi init xong
        self.startup_notified = False
        
    def onEvent(self,event_data,event_type):
        welcome(self,event_data,event_type)
        
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        # Gửi thông báo khởi động lần đầu nhận message (đảm bảo bot đã connect)
        if not self.startup_notified:
            self.startup_notified = True
            # Chạy trong thread riêng để không block message processing
            threading.Thread(target=self._send_startup_notification, daemon=True).start()
        
        print(f"{Fore.GREEN}{Style.BRIGHT}------------------------------\n"
              f"**Message Details:**\n"
              f"- **Message:** {Style.BRIGHT}{message} {Style.NORMAL}\n"
              f"- **Author ID:** {Fore.MAGENTA}{Style.BRIGHT}{author_id} {Style.NORMAL}\n"
              f"- **Thread ID:** {Fore.YELLOW}{Style.BRIGHT}{thread_id}{Style.NORMAL}\n"
              f"- **Thread Type:** {Fore.BLUE}{Style.BRIGHT}{thread_type}{Style.NORMAL}\n"
              f"- **Message Object:** {Fore.RED}{Style.BRIGHT}{message_object}{Style.NORMAL}\n"
              f"{Fore.GREEN}{Style.BRIGHT}------------------------------\n"
              )
        allowed_thread_ids = get_allowed_thread_ids()
        if thread_id in allowed_thread_ids and thread_type == ThreadType.GROUP and not is_admin(author_id):
            handle_check_profanity(self, author_id, thread_id, message_object, thread_type, message)
        try:
            if isinstance(message,str):
                
                self.command_handler.handle_command(message, author_id, message_object, thread_id, thread_type)
        except:
            pass

    def _send_startup_notification(self):
        """Gửi thông báo khởi động trong thread riêng"""
        try:
            # Đợi 2 giây để đảm bảo bot đã ổn định
            time.sleep(2)
            notify_bot_startup(self)
        except Exception as e:
            print(f"❌ Lỗi gửi thông báo khởi động: {e}")

    def force_startup_notification(self):
        """Gửi thông báo khởi động ngay lập tức (dùng cho testing)"""
        try:
            notify_bot_startup(self)
            self.startup_notified = True
            print("✅ Đã gửi thông báo khởi động thủ công")
        except Exception as e:
            print(f"❌ Lỗi gửi thông báo khởi động thủ công: {e}")

def main():
    """Hàm main với error handling"""
    try:
        print(f"{Fore.GREEN}{Style.BRIGHT}🚀 Đang khởi động bot...{Style.RESET_ALL}")
        client = Client(API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES)
        
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ Bot đã khởi tạo thành công!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}📡 Đang kết nối và lắng nghe tin nhắn...{Style.RESET_ALL}")
        
        # Có thể gửi thông báo ngay khi khởi động nếu muốn
        # client.force_startup_notification()
        
        client.listen(thread=True,delay=0)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}🛑 Bot đang tắt theo yêu cầu người dùng...{Style.RESET_ALL}")
        try:
            # Gửi thông báo tắt bot nếu cần
            from modules.startup_notify import send_shutdown_notification
            send_shutdown_notification(client)
        except:
            pass
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Lỗi khởi động bot: {e}{Style.RESET_ALL}")
        
        # Thử gửi thông báo lỗi đến admin
        try:
            from modules.startup_notify import send_startup_error
            send_startup_error(str(e))
        except:
            pass

if __name__ == "__main__":
    main()
