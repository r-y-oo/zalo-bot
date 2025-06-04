from zlapi.models import Message

def handle_id_command(message, message_object, thread_id, thread_type, author_id, client):
    user_id = author_id

    response_message = f"{user_id}"

    message_to_send = Message(text=response_message)

    client.replyMessage(message_to_send, message_object, thread_id, thread_type)
    
def get_mitaizl():
    return {
        'id': handle_id_command
    }
