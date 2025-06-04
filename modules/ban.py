from zlapi.models import Message
from config import ADMIN
import time 

des = {
    'version': "1.1.0",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': "Ban member from group <user_id or tag or reply>",
}

def handle_ban_user_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    group_info = client.fetchGroupInfo(thread_id)

    if not group_info:
        error_message = Message(text="Không thể lấy thông tin nhóm.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    group_data = group_info.gridInfoMap.get(thread_id)

    if not group_data:
        error_message = Message(text="Không tìm thấy thông tin nhóm.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    creator_id = group_data.get('creatorId')
    admin_ids = group_data.get('adminIds', [])

    if admin_ids is None:
        admin_ids = []

    all_admin_ids = set(admin_ids)
    all_admin_ids.add(creator_id)
    all_admin_ids.update(ADMIN)

    user_id = None

    if message_object.mentions:
        user_id = message_object.mentions[0]['uid']
    elif message_object.quote:
        user_id = str(message_object.quote.ownerId)
    else:
        if len(text) < 2:
            error_message = Message(text="Vui lòng tag, reply tin nhắn, uid người cần ban.")
            client.sendMessage(error_message, thread_id, thread_type)
            return
        user_id = text[1]

    if author_id not in all_admin_ids and author_id not in ADMIN:
        error_message = Message(text="Bạn không có quyền thực hiện hành động này!")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    try:
        author_info = client.fetchUserInfo(user_id)
        if isinstance(author_info, dict) and 'changed_profiles' in author_info:
            user_data = author_info['changed_profiles'].get(user_id, {})
            user_name = user_data.get('zaloName', ' không xác định')
        else:
            user_name = "Người dùng không xác định"

    except Exception as e:
        user_name = "Người dùng không xác định"
    
    try:
        if hasattr(client, 'blockUsersInGroup'):
            response = client.blockUsersInGroup(user_id, thread_id)
            send_message = f"Đã kick thành công {user_name}  ra khỏi nhóm."
        else:
            send_message = "deo biet loi gi nua "

    except Exception as e:
        send_message = f"Lỗi khi sút 1 con chó : {str(e)}"

    gui = Message(text=send_message)
    client.sendMessage(gui, thread_id, thread_type)

def get_mitaizl():
    return {
        'ban': handle_ban_user_command
    }