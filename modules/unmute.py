from zlapi.models import Message, Mention, MultiMsgStyle, MessageStyle
from config import ADMIN
ADMIN_ID = ADMIN
des = {
    'version': "1.0.1",
    'credits': "TRBAYK (NGSON) x Quốc Khánh ",
    'description': "Tag tên thành viên trong nhóm"
}
def handle_unmute_command(message, message_object, thread_id, thread_type, author_id, client):
   #     if message.startswith(client + "unmute"):
        
         if author_id not in ADMIN:
            
            msg = "• Bạn Không Có Quyền! Chỉ có admin mới có thể sử dụng được lệnh này."
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=2, style="color", color="#f38ba8", auto_format=False),
                MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
                MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
            ])
            
            client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type,ttl=10000)
            return
        
         if message_object.mentions:
            
            user_id = str(message_object.mentions[0].uid)
        
         elif message_object.quocte:
            
            user_id = str(message_object.quote.ownerId)
        
         else:
            
            msg = f"• Không thể xoá người dùng khỏi danh sách mute vì cú pháp không hợp lệ!\n\n| Command: unmute <tag/reply>"
            example_usage = msg.splitlines()[-1]
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=2, style="color", color="#f38ba8", auto_format=False),
                MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
                MessageStyle(offset=msg.find(example_usage), length=11, style="bold", auto_format=False),
                MessageStyle(offset=msg.find(example_usage), length=1, style="color", color="#585b70", auto_format=False),
                MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
            ])
            
            client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type,ttl=10000)
            return
        
         if not client.is_mute_list.get(thread_id):
            client.is_mute_list[thread_id] = []
        
         if user_id not in client.is_mute_list[thread_id]:
            
            msg = f"• @mention Không có trong danh sách mute!"
            mention = Mention(user_id, offset=2, length=8)
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=1, style="color", color="#fab387", auto_format=False),
                MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
                MessageStyle(offset=2, length=8, style="color", color="#89b4fa", auto_format=False),
                MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
            ])
        
         else:
            
            client.is_mute_list[thread_id].remove(user_id)
            
            msg = f"• Đã xoá @mention khỏi danh sách mute."
            offset_mention = msg.find("@mention")
            mention = Mention(user_id, offset=offset_mention, length=8)
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=2, style="color", color="#a6e3a1", auto_format=False),
                MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
                MessageStyle(offset=offset_mention, length=8, style="color", color="#89b4fa", auto_format=False),
                MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
            ])
        
         client.replyMessage(Message(text=msg, style=styles, mention=mention), message_object, thread_id, thread_type,ttl=10000)
def get_mitaizl():
    return {
        'unmute': handle_unmute_command
    }