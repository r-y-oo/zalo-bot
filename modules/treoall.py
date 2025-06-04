from zlapi.models import *
import os
import time
import threading
from zlapi.models import MultiMsgStyle, Mention, MessageStyle
from config import ADMIN

is_reo_running = False

des = {
    'version': "1.0.2",
    'credits': "Dzi x Tool",
    'description': "Chửi chết cụ 1 con chó được tag"
}

def sua(self, client, args, mid, author_id, message, message_object, thread_id, thread_type):
        delay = 1#ae muốn treoall nhanh ntn thì ae chỉnh ở đây nhé
        try:
            if args == ["stop"]:
                if thread_id in self.threads:
                    self.threads[thread_id][0].set() 
                    self.threads[thread_id][1].join()  
                    del self.threads[thread_id]
                    client.send(Message("Đã dừng lệnh treoall."), thread_id=thread_id, thread_type=thread_type)
                    print(f"Stopped treoall on {thread_id}.")
                else:
                    client.send(Message("Không diễn ra active all."), thread_id=thread_id, thread_type=thread_type)
                    print(f"No active all to stop on {thread_id}.")
                return

            text = " ".join(args)

            def send_all(stop_event):
                while True:
                    if stop_event.is_set():
                        break
                    client.send(Message(text=text, mention=Mention(uid="-1", length=len(text))), thread_id=thread_id, thread_type=thread_type)
                    time.sleep(delay)

            stop_event = threading.Event()
            thread = threading.Thread(target=send_all, args=(stop_event,))
            thread.start()
            self.threads[thread_id] = (stop_event, thread)

        except ValueError:
            client.send(Message("Không hợp lệ. Xin vui lòng thử lại"), thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'treoall': get_mitaizl
    }