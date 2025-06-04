from zlapi.models import Message, MultiMsgStyle, MessageStyle
from config import PREFIX
from config import ADMIN
ADMIN_ID = ADMIN
des = {
    'version': "1.0.2",
    'credits': "Quốc Khánh x Nguyễn Đức Tài",
    'description': "Xoá tin nhắn người dùng"
}

def handle_del_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        msg = "• Mày Không Có Quyền! Chỉ có 𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 mới có thể sử dụng lệnh này."
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#f38ba8", auto_format=False),
            MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
        ])
        client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type)
        return

    if message_object.quote:
        msg2del = message_object.quote
        user_id = str(msg2del.ownerId)
    else:
        msg = f"• Không thể xoá tin nhắn vì cú pháp không hợp lệ!\n\n| Command: {PREFIX}delete <reply tin nhắn cần xoá>"
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#f38ba8", auto_format=False),
            MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
            MessageStyle(offset=msg.find("Command:"), length=11, style="bold", auto_format=False),
            MessageStyle(offset=msg.find("Command:"), length=1, style="color", color="#585b70", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
        ])
        client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type)
        return

    deleted_msg = client.deleteGroupMsg(msg2del.globalMsgId, user_id, msg2del.cliMsgId, thread_id)
    if deleted_msg.status == 0:
        msg = "• Đã xoá tin nhắn của người dùng được reply."
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#a6e3a1", auto_format=False),
            MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
        ])
        client.send(Message(text=msg, style=styles), thread_id, thread_type)
    else:
        msg = "• NhatMinh Ơi Bạn Kco Key Trong Nhóm Nên Bạn Kh Thẻ Xoá Tin Nhắn này."
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=2, style="color", color="#fab387", auto_format=False),
            MessageStyle(offset=2, length=len(msg)-2, style="color", color="#cdd6f4", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False)
        ])
        client.send(Message(text=msg, style=styles), thread_id, thread_type)

def get_mitaizl():
    return {
        'del': handle_del_command
    }
