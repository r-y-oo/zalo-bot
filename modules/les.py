from zlapi.models import MultiMsgStyle, Mention,MessageStyle
from zlapi.models import Message
import random
des = {
    'version': "1.0.0",
    'credits': "Quốc Khánh",
    'description': "check ti le dong tinh cua nu"
}
def handle_les_command(message, message_object, thread_id, thread_type, author_id, client):

            if not message_object.mentions:
                client.replyMessage(Message(text='Vui lòng đề cập đến một người dùng.'), message_object, thread_id=thread_id, thread_type=thread_id)
            else:
                user_id = message_object.mentions[0]['uid']
                probability = random.randint(0, 100)  
                response = f"• Khả năng <@{user_id}> bị les là {probability}%."
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=2, style="color", color="#a24ffb", auto_format=False),
                MessageStyle(offset=2, length=len(response)-2, style="color", color="#ffaf00", auto_format=False),
                MessageStyle(offset=0, length=len(response), style="font", size="13", auto_format=False)
            ])
            mention = Mention(user_id, length=len(f"<@{user_id}>"), offset=response.index(f"<@{user_id}>"))
                
            client.replyMessage(Message(text=response, mention=mention,style=styles), message_object, thread_id=thread_id, thread_type=thread_type)
def get_mitaizl():
    return {
        'les': handle_les_command
    }