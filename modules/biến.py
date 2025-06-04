from zlapi.models import Message

des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜 ",
    'description': "kick member <tag>"
}

def handle_kick_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        client.replyMessage(
            Message(text="🚫 **Bạn không có quyền để thực hiện điều này!**"),
            message_object, thread_id, thread_type
        )
        return

    if message_object.mentions:
        tagged_users = message_object.mentions[0]['uid']
    else:
        tagged_users = author_id

    client.kickUsersFromGroup(tagged_users, thread_id)
    client.blockUsersInGroup( tagged_users, thread_id)

def get_mitaizl():
    return {
        'biến': handle_kick_command
    }