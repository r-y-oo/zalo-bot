#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test để kiểm tra việc load modules noprefix
"""

import sys
import os
sys.path.append('.')

def test_noprefix_loading():
    print("=" * 60)
    print("🔍 KIỂM TRA NOPREFIX MODULES LOADING")
    print("=" * 60)
    
    try:
        from mitaizl import CommandHandler
        
        # Mock client class để test
        class MockClient:
            def __init__(self):
                self.uid = "test_bot_id"
            
            def replyMessage(self, message, message_object, thread_id, thread_type, ttl=None):
                print(f"[BOT REPLY] {message.text}")
            
            def sendMessage(self, text, thread_id, thread_type):
                print(f"[BOT SEND] {text}")
            
            def sendSticker(self, **kwargs):
                print(f"[BOT STICKER] Sent sticker")
        
        # Tạo mock client và command handler
        mock_client = MockClient()
        handler = CommandHandler(mock_client)
        
        print(f"\n📊 Thống kê load modules:")
        print(f"   - Commands có prefix: {len(handler.mitaizl)}")
        print(f"   - Commands noprefix: {len(handler.auto_mitaizl)}")
        
        print(f"\n📝 Danh sách commands noprefix đã load:")
        if handler.auto_mitaizl:
            for i, command in enumerate(handler.auto_mitaizl.keys(), 1):
                print(f"   {i:2d}. '{command}'")
        else:
            print("   ❌ Không có commands nào được load!")
            return False
        
        print(f"\n🧪 Test thử một số commands:")
        
        # Test commands
        test_cases = [
            "hello",
            "hi", 
            "chào",
            "bot",
            "xin chào",
            "alo",
            "system"
        ]
        
        success_count = 0
        for test_command in test_cases:
            print(f"\n   Testing: '{test_command}'")
            if test_command.lower() in handler.auto_mitaizl:
                print(f"   ✅ Command '{test_command}' được nhận diện")
                success_count += 1
                try:
                    # Test một số commands an toàn
                    if test_command.lower() in ['hello', 'hi', 'chào', 'bot']:
                        handler.auto_mitaizl[test_command.lower()](
                            test_command, 
                            {"fake": "message_object"}, 
                            "test_thread_id", 
                            "test_thread_type", 
                            "test_author_id", 
                            mock_client
                        )
                        print(f"   ✅ Thực thi thành công!")
                    else:
                        print(f"   ⚠️  Bỏ qua test thực thi cho command này")
                except Exception as e:
                    print(f"   ⚠️  Lỗi khi thực thi: {e}")
            else:
                print(f"   ❌ Command '{test_command}' không được nhận diện")
        
        print(f"\n📈 Kết quả:")
        print(f"   - Tổng commands test: {len(test_cases)}")
        print(f"   - Commands nhận diện được: {success_count}")
        print(f"   - Tỷ lệ thành công: {success_count/len(test_cases)*100:.1f}%")
        
        return success_count > 0
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
        return False

def test_individual_modules():
    print("\n" + "=" * 60)
    print("🔍 KIỂM TRA TỪNG MODULE NOPREFIX")
    print("=" * 60)
    
    noprefix_folder = 'modules/noprefix'
    if not os.path.exists(noprefix_folder):
        print(f"❌ Folder {noprefix_folder} không tồn tại!")
        return False
    
    success_count = 0
    total_count = 0
    
    for filename in os.listdir(noprefix_folder):
        if filename.endswith('.py') and filename != '__init__.py':
            total_count += 1
            module_name = filename[:-3]
            print(f"\n🔍 Kiểm tra module: {module_name}")
            
            try:
                module = __import__(f'modules.noprefix.{module_name}', fromlist=[''])
                if hasattr(module, 'get_mitaizl'):
                    commands = module.get_mitaizl()
                    print(f"   ✅ Module {module_name} có {len(commands)} commands: {list(commands.keys())}")
                    success_count += 1
                else:
                    print(f"   ⚠️  Module {module_name} không có hàm get_mitaizl()")
            except Exception as e:
                print(f"   ❌ Lỗi load module {module_name}: {e}")
    
    print(f"\n📈 Kết quả kiểm tra modules:")
    print(f"   - Tổng modules: {total_count}")
    print(f"   - Modules load thành công: {success_count}")
    print(f"   - Tỷ lệ thành công: {success_count/total_count*100:.1f}%" if total_count > 0 else "   - Không có module nào")
    
    return success_count > 0

if __name__ == "__main__":
    print("🚀 Bắt đầu test noprefix system...")
    
    # Test individual modules first
    modules_ok = test_individual_modules()
    
    # Test loading system
    loading_ok = test_noprefix_loading()
    
    print("\n" + "=" * 60)
    if modules_ok and loading_ok:
        print("✅ TẤT CẢ TESTS THÀNH CÔNG!")
        print("🎉 Hệ thống noprefix đã hoạt động bình thường!")
    else:
        print("❌ CÓ VẤN ĐỀ XẢY RA!")
        if not modules_ok:
            print("   - Lỗi load individual modules")
        if not loading_ok:
            print("   - Lỗi load hệ thống tổng thể")
    print("=" * 60)