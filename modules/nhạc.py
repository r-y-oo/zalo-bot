import os
import random
import re
import time
import requests
from zlapi import *
from zlapi.models import *
from bs4 import BeautifulSoup
from fake_useragent import UserAgent 

des = {
    'version': "1.x.x",
    'credits': "DzixTool",
    'description': "Nhạc"
}

def handle_nhac_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()
    
    # Tạo và gửi tin nhắn
    action = "✅"
    client.sendReaction(message_object, action, thread_id, thread_type, reactionType=75)

    if len(content) < 2:
        error_message = Message(text="𝑉𝑢𝑖 𝐿𝑜𝑛𝑔 𝑁ℎ𝑎𝑝 𝑇𝑒𝑛 𝐵𝑎𝑖 𝐻𝑎𝑡 𝐷𝑒 𝐵𝑜𝑡 𝑇𝑖𝑚 𝐾𝑖𝑒𝑚 𝑐ℎ𝑜 𝐵𝑎𝑛‼️")
        client.replyMessage(error_message, message_object, thread_id, thread_type,ttl=6000000000)
        return

    tenbaihat = ' '.join(content[1:]) 

    def get_client_id():
        """Lấy client ID từ SoundCloud và lưu vào tệp nếu chưa có."""
        client_id_file = 'client_id.txt'
        
        # Xóa client_id cũ nếu có để lấy mới
        if os.path.exists(client_id_file):
            try:
                os.remove(client_id_file)
                print("Đã xóa client_id cũ, đang lấy client_id mới...")
            except:
                pass

        try:
            res = requests.get('https://soundcloud.com/', headers=get_headers(), timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            script_tags = soup.find_all('script', {'crossorigin': True})
            urls = [tag.get('src') for tag in script_tags if tag.get('src') and tag.get('src').startswith('https')]
            if not urls:
                raise Exception('Không tìm thấy URL script')
            
            res = requests.get(urls[-1], headers=get_headers(), timeout=10)
            res.raise_for_status()
            
            # Tìm client_id bằng nhiều cách khác nhau
            client_id = None
            patterns = [
                r',client_id:"([^"]+)"',
                r'"client_id":"([^"]+)"',
                r'client_id:"([^"]+)"',
                r'client_id=([a-zA-Z0-9]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, res.text)
                if match:
                    client_id = match.group(1)
                    break
            
            if not client_id:
                raise Exception('Không tìm thấy client_id trong script')

            # Lưu client_id vào tệp
            with open(client_id_file, 'w') as file:
                file.write(client_id)
            
            print(f"Đã lấy client_id mới: {client_id[:10]}...")
            return client_id
            
        except Exception as e:
            print(f"Không thể lấy client ID: {e}")
            # Thử sử dụng client_id mặc định
            default_client_ids = [
                'FZ4N7j5n7REhvxORW9Arr4NPHiWN2Tcu',
                'iZIs9mchVcX5lhVRyQGGAYlNPVldzAoJ',
                'c3a076e7ac6b0b759e8b1040ba2af808'
            ]
            
            for default_id in default_client_ids:
                try:
                    # Test client_id
                    test_url = f'https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/soundcloud&client_id={default_id}'
                    test_response = requests.get(test_url, headers=get_headers(), timeout=5)
                    if test_response.status_code == 200:
                        with open(client_id_file, 'w') as file:
                            file.write(default_id)
                        print(f"Sử dụng client_id mặc định: {default_id[:10]}...")
                        return default_id
                except:
                    continue
            
            error_message = Message(text="❌ Không thể lấy client ID. API SoundCloud có thể đã thay đổi.")
            client.replyMessage(error_message, message_object, thread_id, thread_type)
            return None

    def wait_for_client_id():
        """Đợi cho đến khi lấy được client ID từ SoundCloud."""
        max_attempts = 3
        for attempt in range(max_attempts):
            client_id = get_client_id()
            if client_id:
                return client_id
            print(f"Lần thử {attempt + 1}/{max_attempts} - Đang chờ client ID...")
            if attempt < max_attempts - 1:
                time.sleep(2)  # Đợi 2 giây trước khi thử lại
        return None

    def get_headers():
        """Tạo tiêu đề ngẫu nhiên cho yêu cầu HTTP."""
        user_agent = UserAgent()
        headers = {
            "User-Agent": user_agent.random,
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "fr-FR,fr;q=0.9",
                "es-ES,es;q=0.9",
                "de-DE,de;q=0.9",
                "zh-CN,zh;q=0.9"
            ]),
            "Referer": 'https://soundcloud.com/',
            "Upgrade-Insecure-Requests": "1"
        }
        return headers 

    def search_song(query):
        """Tìm kiếm bài hát trên SoundCloud và trả về URL, tiêu đề và ảnh bìa của bài hát đầu tiên tìm thấy."""
        try:
            link_url = 'https://soundcloud.com'
            headers = get_headers()
            search_url = f'https://m.soundcloud.com/search?q={requests.utils.quote(query)}'
            messagesend = Message(text="𝘉𝘰𝘵 𝘋𝘢𝘯𝘨 𝘛𝘪𝘮 𝘒𝘪𝘦𝘮 𝘋𝘶𝘢 𝘛𝘳𝘦𝘯 𝘛𝘩𝘰𝘯𝘨 𝘛𝘪𝘯𝘩 𝘔𝘢 𝘉𝘢𝘯 𝘕𝘩𝘢𝘱♡")
            client.replyMessage(messagesend, message_object, thread_id, thread_type,ttl=2000000000000000)
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            url_pattern = re.compile(r'^/[^/]+/[^/]+$')
            for element in soup.select('div > ul > li > div'):
                a_tag = element.select_one('a')
                if a_tag and a_tag.has_attr('href'):
                    relative_url = a_tag['href']
                    if url_pattern.match(relative_url):
                        title = a_tag.get('aria-label', '')
                        url = link_url + relative_url
                        img_tag = element.select_one('img')
                        if img_tag and img_tag.has_attr('src'):
                            cover_url = img_tag['src']
                        else:
                            cover_url = None 
                    
                        return url, title, cover_url
            return None, None, None
        except Exception as e:
            print(f"Lỗi khi tìm kiếm bài hát: {e}")
            return None, None, None

    def download(link):
        """Lấy và in ra URL âm thanh từ SoundCloud."""
        try:
            client_id = wait_for_client_id()  # Đợi cho đến khi lấy được client_id
            if not client_id:
                print("Không thể lấy client_id")
                return None
                
            headers = get_headers()
            api_url = f'https://api-v2.soundcloud.com/resolve?url={link}&client_id={client_id}'
            print(f"Đang gọi API: {api_url}")
            
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Kiểm tra xem có dữ liệu media không
            if 'media' not in data or 'transcodings' not in data['media']:
                print("Không tìm thấy dữ liệu media trong phản hồi")
                return None
            
            # Tìm URL progressive (MP3)
            progressive_url = None
            transcodings = data['media']['transcodings']
            
            for transcoding in transcodings:
                if (transcoding.get('format', {}).get('protocol') == 'progressive' and
                    'mp3' in transcoding.get('format', {}).get('mime_type', '').lower()):
                    progressive_url = transcoding['url']
                    break
            
            if not progressive_url:
                # Thử tìm bất kỳ URL progressive nào
                progressive_url = next((t['url'] for t in transcodings if t['format']['protocol'] == 'progressive'), None)
            
            if not progressive_url:
                print("Không tìm thấy URL âm thanh progressive")
                return None
            
            # Lấy URL âm thanh thực tế
            auth_param = f"&track_authorization={data.get('track_authorization', '')}" if data.get('track_authorization') else ""
            final_url = f'{progressive_url}?client_id={client_id}{auth_param}'
            
            response = requests.get(final_url, headers=headers, timeout=10)
            response.raise_for_status()
            url_data = response.json()
            final_audio_url = url_data.get('url')
            
            if not final_audio_url:
                print("Không lấy được URL âm thanh cuối cùng")
                return None
                
            print(f"Đã lấy được URL âm thanh: {final_audio_url[:50]}...")
            return final_audio_url
            
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối khi tải âm thanh: {e}")
            return None
        except Exception as e:
            print(f"Lỗi khi tải âm thanh: {e}")
            return None

    def save_file_to_cache(url, filename):
        """Tải và lưu file vào thư mục con cache."""
        try:
            response = requests.get(url, headers=get_headers())
            response.raise_for_status()
            cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
            os.makedirs(cache_dir, exist_ok=True)
            file_path = os.path.join(cache_dir, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            print(f"Tải file thành công! Đã lưu tại {file_path}")
            return file_path
        except Exception as e:
            print(f"Lỗi khi tải file: {e}")
            return None

    def upload_to_uguu(file_path):
        """Tải lên tệp tới Uguu.se và trả về URL."""
        url = "https://uguu.se/upload"
        try:
            with open(file_path, 'rb') as file:
                files = {'files[]': (os.path.basename(file_path), file)}
                response = requests.post(url, files=files, headers=get_headers())
                response.raise_for_status()
            response_text = response.text
            if "https:" in response_text:
                start = response_text.find("https:")
                end = response_text.find(" ", start)
                if end == -1:
                    end = len(response_text)
                url = response_text[start:end]
                return url.replace("\\", "")  
            else:
                return "Không tìm thấy URL trong phản hồi."
        except Exception as e:
            print(f"Lỗi khi tải lên: {e}")
            return None

    def delete_file(file_path):
        """Xóa tệp sau khi sử dụng."""
        try:
            os.remove(file_path)
            print(f"Đã xóa tệp: {file_path}")
        except Exception as e:
            print(f"Lỗi khi xóa tệp: {e}")

    if tenbaihat:
        print(f"Tên bài hát tìm thấy: {tenbaihat}")
        link, title, cover = search_song(tenbaihat)
        if link:
            print(f"URL bài hát tìm thấy: {link}")
            
            # Lấy URL âm thanh
            audio_url = download(link)
            
            if audio_url:
                # Tải file âm thanh
                mp3_file = save_file_to_cache(audio_url, 'downloaded_file.mp3')
                if mp3_file:
                    upload_response = upload_to_uguu(mp3_file)
                    
                    if upload_response and upload_response != "Không tìm thấy URL trong phản hồi.":
                        ulrp = upload_response.replace('"', '').replace(',', '')
                        
                        # Xử lý ảnh bìa
                        cover_file = None
                        if cover:
                            try:
                                cover_response = requests.get(cover, timeout=5)
                                if cover_response.status_code == 200:
                                    cover_filename = cover.rsplit("/", 1)[-1]
                                    if not cover_filename.endswith(('.jpg', '.jpeg', '.png')):
                                        cover_filename += '.jpg'
                                    cover_file = cover_filename
                                    with open(cover_file, "wb") as f:
                                        f.write(cover_response.content)
                            except Exception as e:
                                print(f"Lỗi khi tải ảnh bìa: {e}")
                                cover_file = None
                        
                        # Gửi tin nhắn với thông tin bài hát
                        messagesend = Message(text=f"𝑇𝑒𝑛 𝑏𝑎𝑖 ℎ𝑎𝑡:🐳{title}❄️")
                        
                        if cover_file and os.path.exists(cover_file):
                            try:
                                client.sendLocalImage(cover_file, thread_id, thread_type, message=messagesend, width=240, height=240, ttl=120000000000)
                            except:
                                client.replyMessage(messagesend, message_object, thread_id, thread_type)
                        else:
                            client.replyMessage(messagesend, message_object, thread_id, thread_type)
                        
                        # Gửi file âm thanh
                        try:
                            client.sendRemoteVoice(voiceUrl=ulrp, thread_id=thread_id, thread_type=thread_type, ttl=12000000000000)
                        except Exception as e:
                            print(f"Lỗi khi gửi voice: {e}")
                            error_msg = Message(text="❌ Lỗi khi gửi file âm thanh.")
                            client.replyMessage(error_msg, message_object, thread_id, thread_type)
                        
                        # Dọn dẹp file
                        delete_file(mp3_file)
                        if cover_file and os.path.exists(cover_file):
                            delete_file(cover_file)
                    else:
                        print("Không thể tải lên Uguu.se.")
                        error_msg = Message(text="❌ Không thể tải lên server. Vui lòng thử lại.")
                        client.replyMessage(error_msg, message_object, thread_id, thread_type)
                        delete_file(mp3_file)
                else:
                    print("Không thể tải file âm thanh.")
                    error_msg = Message(text="❌ Không thể tải file âm thanh. Vui lòng thử lại.")
                    client.replyMessage(error_msg, message_object, thread_id, thread_type)
            else:
                print("Không thể lấy URL âm thanh.")
                error_msg = Message(text="❌ Không thể lấy link âm thanh. Bài hát có thể bị hạn chế hoặc không tồn tại.")
                client.replyMessage(error_msg, message_object, thread_id, thread_type)
        else:
            print("Không tìm thấy bài hát.")
            error_msg = Message(text="❌ Không tìm thấy bài hát. Vui lòng thử từ khóa khác.")
            client.replyMessage(error_msg, message_object, thread_id, thread_type)
    else:
        print("Tên bài hát không được bỏ trống.")

def get_mitaizl():
    return {
        'nhạc': handle_nhac_command
    }

