import os
from zlapi.models import Message
import importlib

des = {
    'version': "1.0.2",
    'credits': "Duy Khanh",
    'description': "Xem toàn bộ lệnh hiện có của bot"  
    }
def get_all_mitaizl():
    mitaizl = {}

    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'get_mitaizl'):
                get_mitaizl = module.get_mitaizl()
                mitaizl.update(get_mitaizl)

    command_names = list(mitaizl.keys())
    
    return command_names

def handle_menu_command(message, message_object, thread_id, thread_type, author_id, client):

    command_names = get_all_mitaizl()

    total_mitaizl = len(command_names)
    numbered_mitaizl = [f"{i+1}. {name}" for i, name in enumerate(command_names)]
    menu_message = f"☄️✨️ 🌸𝑃𝑟𝑜𝑓𝑖𝑙𝑒 𝐴𝑑𝑚𝑖𝑛 🌸 ✨️☄️\n---kduy9060@𝐠𝐦𝐚𝐢𝐥.𝐜𝐨𝐦---\nUser Name: Duy Khanh \nBirthday: 28/04/2???\nGiới Tính: Nam🧏\n-ˋˏ✄┈┈┈┈\n 🌐WEBSITE : https://pather.uk/ \n 💻ICLUOD: kduy9060@gmail.com\n/-li From:Việt Nam /-flag\n---- 🌸𝐋𝐨𝐚𝐝𝐢𝐧𝐠 Duy Khanh🌸 ----\n🌐 Lưu ý: Thắc mắc liên hệ trực tiếp với Admin được hỗ trợ.\n📉Xu Hướng Tuyệt Đối📊\n💤 Cảm ơn bạn đã quan tâm! 💤\n👋️ Nếu bạn cần giúp đỡ, hãy liên hệ với admin ❗\n🎨 𝘊𝘰𝘱𝘺𝘙𝘪𝘨𝘩𝘵 𝘈𝘥𝘮𝘪𝘯 Duy Khanh💦💸\nCheck Imei/Ck Duy Khanh🔱 - Tool"

    client.sendLocalImage("9.jpg", thread_id=thread_id, thread_type=thread_type, message=Message(text=menu_message),ttl=120000000)
    
def get_mitaizl():
    return {
        'advip': handle_menu_command
    }