from zlapi.models import Message, Mention, ZaloAPIException, ThreadType
from config import ADMIN
import time

des = {
    'version': "1.0.1",
    'credits': " ౨ৎƙɵɑɦ🎀",
    'description': "Spam nhóm với nội dung tùy chỉnh"
}

def handle_spnhom_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="🚫 Bạn không có quyền sử dụng lệnh này!"), 
            message_object, thread_id, thread_type
        )
        return
    
    try:
        parts = message.split(" ", 2)
        if len(parts) < 3:
            client.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp link nhóm và nội dung spam!"), 
                message_object, thread_id, thread_type
            )
            return
            
        url = parts[1].strip()
        spam_text = parts[2].strip()
        
        if not url.startswith("https://zalo.me/"):
            client.replyMessage(
                Message(text="⛔ Link không hợp lệ! Link phải bắt đầu bằng https://zalo.me/"), 
                message_object, thread_id, thread_type
            )
            return
        
        join_result = client.joinGroup(url)
        if not join_result:
            raise ZaloAPIException("Không thể tham gia nhóm")
        
        group_info = client.getiGroup(url)
        if not isinstance(group_info, dict) or 'groupId' not in group_info:
            raise ZaloAPIException("Không thể lấy thông tin nhóm")
            
        group_id = group_info['groupId']
        
        spam_count = 10  # Số lần spam
        for _ in range(spam_count):
            mention = Mention("-1", length=len(spam_text), offset=0)
            client.send(
                Message(text=spam_text, mention=mention),
                group_id, ThreadType.GROUP
            )
            time.sleep(0)
        while True:
            mention = Mention("-1", length=len(spam_text), offset=0) 
            client.send(
                Message(text=spam_text, mention=mention),
                group_id, ThreadType.GROUP
            )
            time.sleep(0.00000000000000000000001)

        client.replyMessage(
            Message(text=f"✅ Đang spam với nội dung: {spam_text}\nID nhóm: {group_id}"),
            message_object, thread_id, thread_type
        )
        
    except ZaloAPIException as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi API: {str(e)}"),
            message_object, thread_id, thread_type
        )
    except Exception as e:
        client.replyMessage(
            Message(text=f"❌ Lỗi: {str(e)}"),
            message_object, thread_id, thread_type
        )

def get_mitaizl():
    return {
        'spgr': handle_spnhom_command
    }