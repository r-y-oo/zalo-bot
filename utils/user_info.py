from colorama import Fore
from zlapi import ZaloAPI, ZaloAPIException

def fetch_user_info(client, userId):
    """Fetch user info and return zaloName or displayName."""
    try:
        user_info = client.fetchUserInfo(userId)
        print(f"Fetched user info for {userId}: {user_info}")  # Debug print
        if 'changed_profiles' in user_info and userId in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][userId]
            return profile.get('zaloName', profile.get('displayName', userId))
        return userId
    except Exception as e:
        print(f"{Fore.RED}Error fetching user info: {e}")
        return userId  # Return userId if there is an error


def is_admin(client, thread_id, user_id):
    """Check if a user is an admin in a specific thread."""
    try:
        group_info = client.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']
        return user_id in admin_ids or user_id == creator_id
    except ZaloAPIException as e:
        print(f"{Fore.RED}Error checking admin status: {e}")
        return False
