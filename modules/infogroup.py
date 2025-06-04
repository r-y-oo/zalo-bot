import requests
import os
from zlapi.models import Message, ZaloAPIException

def handle_group_info_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        group_info = client.fetchGroupInfo(thread_id)

        if not isinstance(group_info, dict):
            group_info = group_info.__dict__

        group_name = group_info.get('gridInfoMap', {}).get(thread_id, {}).get('name', 'N/A')
        group_id = group_info.get('gridInfoMap', {}).get(thread_id, {}).get('groupId', 'N/A')
        group_avatar = group_info.get('gridInfoMap', {}).get(thread_id, {}).get('fullAvt', None)

        group_info_message = (f"Group Info:\n"
                              f"Tên nhóm: {group_name}\n"
                              f"ID nhóm: {group_id}\n")

        message_to_send = Message(text=group_info_message)

        if group_avatar:
            image_response = requests.get(group_avatar)
            image_path = 'temp_image.jpeg'

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            client.sendLocalImage(
                image_path, 
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type
            )
            
            os.remove(image_path)
        
    except ZaloAPIException:

        error_message = Message(text="Could not retrieve group info.")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:

        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'infogroup': handle_group_info_command
    }
