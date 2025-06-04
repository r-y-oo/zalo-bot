import json

USERS_FILE = 'users.json'

def load_users():
    """Load user data from the JSON file."""
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save user data to the JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def is_vip(user_id):
    """Check if a user is VIP."""
    users = load_users()
    return users.get('users', {}).get(user_id, 'free') == 'vip'

def set_user_status(user_id, status):
    """Set user status to 'vip' or 'free'."""
    users = load_users()
    users['users'][user_id] = status
    save_users(users)
