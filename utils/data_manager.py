import json

def load_data(data_file):
    """Load user data and message counts from a JSON file."""
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            user_data = data.get('user_data', {})
            message_counts = data.get('message_counts', {})
            return user_data, message_counts
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, {}

def save_data(data_file, user_data, message_counts):
    """Save user data and message counts to a JSON file."""
    with open(data_file, 'w') as f:
        json.dump({'user_data': user_data, 'message_counts': message_counts}, f, indent=4)

# def save_data(self):
#     """Save user data and message counts to a JSON file."""
#     save_data(self.data_file, self.user_data, self.message_counts)  