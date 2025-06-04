def update_message_count(message_counts, thread_id, author_id):
    """Update message count for a specific thread and author."""
    if thread_id not in message_counts:
        message_counts[thread_id] = {}
    if author_id not in message_counts[thread_id]:
        message_counts[thread_id][author_id] = 0
    message_counts[thread_id][author_id] += 1
    
def send_message(client, message, thread_id, author_id):
    # Giả định phương thức này để gửi tin nhắn đến thread_id
    print(f"Sending message to {thread_id}: {message}")