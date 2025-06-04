import json
import os
from zlapi.models import Message, ThreadType
from colorama import Fore
des = {
    'version': "1.0.2",
    'credits': "𝙃𝙖̀ 𝙃𝙪𝙮 𝙃𝙤𝙖̀𝙣𝙜",
    'description': " Tiện Ích"
}

# Path to the configuration file
CONFIG_PATH = 'config.json'

def load_config():
    """Load the configuration from the JSON file."""
    if not os.path.exists(CONFIG_PATH):
        config = {
            "ADMINBOT": ["8499074262308020780"],
            "NDH": ["8499074262308020780"],
            "adminOnly": False,
            "adminPaseOnly": False,
            "ndhOnly": False
        }
        save_config(config)
    else:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    return config

def save_config(config):
    """Save the configuration to the JSON file."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def handle_admin(client, message_object, thread_id, author_id, thread_type):
    """Handle the admin command to manage admins and support roles."""
    if hasattr(message_object, 'content') and isinstance(message_object.content, str):
        if message_object.content.startswith('admin'):
            args = message_object.content.split()[1:]  # Split the command arguments
            config = load_config()

            if len(args) == 0:
                client.send(Message(
                    text=(
                        "🔧 [ADMIN CONFIG SETTING] 🔧\n"
                        "──────────────────\n"
                        "💼 `admin add` -> Thêm người dùng làm admin\n"
                        "🛠 `admin remove` -> Gỡ vai trò admin\n"
                        "🛡 `admin sp` -> Thêm người dùng làm người điều hành\n"
                        "⚔️ `admin resp` -> Gỡ vai trò người điều hành\n"
                        "📋 `admin list` -> Xem danh sách admin và người điều hành\n"
                        "⚙️ `admin qtvonly` -> Bật/tắt chế độ quản trị viên\n"
                        "🔒 `admin pa` -> Bật/tắt chế độ Người điều hành\n"
                        "🔐 `admin only` -> Bật/tắt chế độ chỉ admin sử dụng bot\n"
                        "───────────────────"
                    )
                ), thread_id=thread_id, thread_type=thread_type)
                return

            subcommand = args[0].lower()

            # Handle the list subcommand
            if subcommand == 'list':
                admin_list = config.get("ADMINBOT", [])
                ndh_list = config.get("NDH", [])

                admin_msg = "\n".join([f"👤 Admin ID: {admin_id}" for admin_id in admin_list])
                ndh_msg = "\n".join([f"👤 NDH ID: {ndh_id}" for ndh_id in ndh_list])

                response_text = (
                    f"📋 [Danh Sách Admin] 📋\n{admin_msg}\n\n"
                    f"📋 [Danh Sách Người Điều Hành] 📋\n{ndh_msg}"
                )
                client.send(Message(text=response_text), thread_id=thread_id, thread_type=thread_type)

            # Handle the add admin subcommand
            elif subcommand == 'add':
                if author_id not in config["ADMINBOT"]:
                    client.send(Message(
                        text="⛔ Bạn không có quyền thêm admin."
                    ), thread_id=thread_id, thread_type=thread_type)
                    return

                new_admin_id = args[1]
                if new_admin_id not in config["ADMINBOT"]:
                    config["ADMINBOT"].append(new_admin_id)
                    save_config(config)
                    client.send(Message(
                        text=f"✅ **Đã thêm admin**: {new_admin_id}"
                    ), thread_id=thread_id, thread_type=thread_type)
                else:
                    client.send(Message(
                        text=f"⚠️ **Người dùng {new_admin_id} đã là admin.**"
                    ), thread_id=thread_id, thread_type=thread_type)

            # Handle the remove admin subcommand
            elif subcommand in ['remove', 'rm', 'delete']:
                if author_id not in config["ADMINBOT"]:
                    client.send(Message(
                        text="⛔ **Bạn không có quyền gỡ bỏ admin.**"
                    ), thread_id=thread_id, thread_type=thread_type)
                    return

                admin_to_remove = args[1]
                if admin_to_remove in config["ADMINBOT"]:
                    config["ADMINBOT"].remove(admin_to_remove)
                    save_config(config)
                    client.send(Message(
                        text=f"✅ **Đã gỡ bỏ admin**: {admin_to_remove}"
                    ), thread_id=thread_id, thread_type=thread_type)
                else:
                    client.send(Message(
                        text=f"⚠️ **Người dùng {admin_to_remove} không phải là admin.**"
                    ), thread_id=thread_id, thread_type=thread_type)

            # Handle the add support role subcommand
            elif subcommand == 'sp':
                if author_id not in config["ADMINBOT"]:
                    client.send(Message(
                        text="⛔ **Bạn không có quyền thêm người điều hành.**"
                    ), thread_id=thread_id, thread_type=thread_type)
                    return

                new_ndh_id = args[1]
                if new_ndh_id not in config["NDH"]:
                    config["NDH"].append(new_ndh_id)
                    save_config(config)
                    client.send(Message(
                        text=f"✅ **Đã thêm người điều hành**: {new_ndh_id}"
                    ), thread_id=thread_id, thread_type=thread_type)
                else:
                    client.send(Message(
                        text=f"⚠️ **Người dùng {new_ndh_id} đã là người điều hành.**"
                    ), thread_id=thread_id, thread_type=thread_type)

            # Handle the remove support role subcommand
            elif subcommand == 'resp':
                if author_id not in config["ADMINBOT"]:
                    client.send(Message(
                        text="⛔ **Bạn không có quyền gỡ bỏ người điều hành.**"
                    ), thread_id=thread_id, thread_type=thread_type)
                    return

                ndh_to_remove = args[1]
                if ndh_to_remove in config["NDH"]:
                    config["NDH"].remove(ndh_to_remove)
                    save_config(config)
                    client.send(Message(
                        text=f"✅ **Đã gỡ bỏ người điều hành**: {ndh_to_remove}"
                    ), thread_id=thread_id, thread_type=thread_type)
                else:
                    client.send(Message(
                        text=f"⚠️ **Người dùng {ndh_to_remove} không phải là người điều hành.**"
                    ), thread_id=thread_id, thread_type=thread_type)

            # Handle the toggle qtvonly subcommand
            elif subcommand == 'qtvonly':
                config["adminOnly"] = not config["adminOnly"]
                save_config(config)
                status = "bật" if config["adminOnly"] else "tắt"
                client.send(Message(
                    text=f"🔄 **Chế độ chỉ Quản trị viên sử dụng bot đã {status}.**"
                ), thread_id=thread_id, thread_type=thread_type)

            # Handle the toggle admin-only subcommand
            elif subcommand == 'only':
                config["adminOnly"] = not config["adminOnly"]
                save_config(config)
                status = "bật" if config["adminOnly"] else "tắt"
                client.send(Message(
                    text=f"🔄 **Chế độ chỉ Admin dùng được bot đã {status}.**"
                ), thread_id=thread_id, thread_type=thread_type)

            # Handle the toggle adminPaseOnly subcommand
            elif subcommand == 'pa':
                config["adminPaseOnly"] = not config["adminPaseOnly"]
                save_config(config)
                status = "bật" if config["adminPaseOnly"] else "tắt"
                client.send(Message(
                    text=f"🔄 **Chế độ chỉ Admin or Người điều hành mới nhắn riêng với bot đã {status}.**"
                ), thread_id=thread_id, thread_type=thread_type)

            # Handle the toggle ndh-only subcommand
            elif subcommand in ['sponly', '-s']:
                config["ndhOnly"] = not config["ndhOnly"]
                save_config(config)
                status = "bật" if config["ndhOnly"] else "tắt"
                client.send(Message(
                    text=f"🔄 **Chế độ chỉ Người điều hành mới dùng được bot đã {status}.**"
                ), thread_id=thread_id, thread_type=thread_type)

            else:
                client.send(Message(
                    text="❌ **Lệnh không hợp lệ. Vui lòng kiểm tra lại.**"
                ), thread_id=thread_id, thread_type=thread_type)

def get_mitaizl():
    return {
        'admin_on': handle_admin
    }
