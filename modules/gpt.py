import requests
import os
from zlapi.models import Message, Mention
import logging
import datetime

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Duy Khang",
    'description': "Hỏi đáp cùng Gemini",
    'power': "Thành viên"
}

GEMINI_API_KEY = "AIzaSyC5VvVGBk3T0TzfF_JCaDTDPAW97oRhdrc"
conversation_states = {}

def handle_gemini_command(message, message_object, thread_id, thread_type, author_id, client):
    user_question = " ".join(message.strip().split()[1:]).strip()
    if not user_question:
        client.replyMessage(Message(text="• Nhập câu hỏi để trò chuyện cùng Gemini."), message_object, thread_id, thread_type, ttl=12000)
        return

    conversation_state = conversation_states.get(thread_id, {'history': []})
    gemini_response = get_gemini_response(user_question, conversation_state, thread_id)

    if gemini_response:
        client.replyMessage(
            Message(text=f"@Member {gemini_response}", mention=Mention(author_id, length=len("@Member"), offset=0)),
            message_object, thread_id, thread_type, ttl=1800000)
    else:
        client.replyMessage(
            Message(text="Không thể lấy câu trả lời từ Chat API.",
                    mention=Mention(author_id, length=len("@Member"), offset=0)),
            message_object, thread_id, thread_type, ttl=1800000)


def get_gemini_response(user_question, conversation_state, thread_id):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = f"Bạn là một trợ lý ảo được tạo ra bởi Duy Khanh, hiện tại là {current_time}.\n"
    prompt += f"Lịch sử cuộc trò chuyện:\n"
    for item in conversation_state['history'][-10:]:
        prompt += f"{item['role']}: {item['text']}\n"
    prompt += f"User: {user_question}\n"
    prompt += ">"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if 'candidates' in result and result['candidates']:
            for candidate in result['candidates']:
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'text' in part:
                            conversation_state['history'].append({'role': 'user', 'text': user_question})
                            conversation_state['history'].append({'role': 'gemini', 'text': part['text']})
                            conversation_states[thread_id] = conversation_state
                            return part['text']
        else:
            logging.error(f"Gemini response is empty or doesn't contain valid 'candidates'. Response: {result}")
            return None
        logging.error(f"Gemini response doesn't have valid text. Response: {result}")
        return None

    except requests.exceptions.RequestException as e:
        status_code = response.status_code if 'response' in locals() else 'N/A'
        logging.error(f"Request Exception: {e}, Status Code: {status_code}, Response: {response.text if 'response' in locals() else 'N/A'}")
        return None
    except Exception as e:
        logging.error(f"General Exception: {e}")
        return None


def get_mitaizl():
    return {
        'gpt': handle_gemini_command
    }