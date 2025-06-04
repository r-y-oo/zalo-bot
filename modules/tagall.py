from zlapi.models import Message, ZaloAPIException, ThreadType, Mention, MultiMention
from config import ADMIN
import time
import random

des = {
    'version': "1.0.1",
    'credits': "HA HUY HOANG",
    'description': "Lệnh tagall nhóm",
    'power': "Quản trị viên Bot"
}

# ID được phép dùng lệnh
ALLOWED_ID = "8499074262308020780"

import time

def handle_tagall_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        if str(author_id) != ALLOWED_ID:
            client.send(
                Message(text="Bạn không có quyền dùng lệnh này."),
                thread_id=thread_id,
                thread_type=ThreadType.GROUP
            )
            return

        parts = message.split(" ", 1)
        if len(parts) < 2:
            return

        tagall_message = parts[1].strip()

        group_info = client.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
        members = group_info.get('memVerList', [])
        if not members:
            return

        total = len(members)
        batch_size = 200
        max_text_length = 2000
        base_text = f"{tagall_message}\n"

        for i in range(0, total, batch_size):
            batch = members[i:i + batch_size]
            text = base_text
            mentions = []
            offset = len(text)

            for member in batch:
                member_parts = member.split('_', 1)
                if len(member_parts) != 2:
                    continue
                user_id, user_name = member_parts
                mention_text = f"{user_name} "
                mention_length = len(mention_text)

                if len(text) + mention_length > max_text_length:
                    # Gửi phần hiện tại
                    client.send(
                        Message(text=text, mention=MultiMention(mentions)),
                        thread_id=thread_id,
                        thread_type=ThreadType.GROUP
                    )
                    time.sleep(1.5)

                    # Reset nội dung mới
                    text = base_text
                    mentions = []
                    offset = len(text)

                mentions.append(Mention(uid=user_id, offset=offset, length=len(user_name), auto_format=False))
                text += mention_text
                offset += mention_length

            # Gửi phần còn lại của batch
            if mentions:
                client.send(
                    Message(text=text, mention=MultiMention(mentions)),
                    thread_id=thread_id,
                    thread_type=ThreadType.GROUP
                )
                time.sleep(1.5)

    except ZaloAPIException as e:
        print(f"Lỗi API: {e}")
    except Exception as e:
        print(f"Lỗi chung: {e}")


def ft_vxkiue():
    return {
        'tagall': handle_tagall_command
    }
