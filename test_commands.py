#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

# Test các lệnh noprefix
from mitaizl import CommandHandler

# Mock client class để test
class MockClient:
    def replyMessage(self, msg, msg_obj, thread_id, thread_type):
        print(f"Reply: {msg.text}")
    
    def sendSticker(self, **kwargs):
        print("Sticker sent")

# Test các lệnh
def test_command(command_text):
    handler = CommandHandler(None)
    handler.client = MockClient()
    
    print(f"\n--- Testing command: '{command_text}' ---")
    print(f"Available commands: {list(handler.auto_mitaizl.keys())}")
    
    # Check if command exists
    if command_text.lower() in handler.auto_mitaizl:
        print(f"✓ Command '{command_text}' found!")
        try:
            # Execute command
            command_func = handler.auto_mitaizl[command_text.lower()]
            command_func(command_text, None, "test_thread", None, "test_author", handler.client)
            print("✓ Command executed successfully!")
        except Exception as e:
            print(f"✗ Error executing command: {e}")
    else:
        print(f"✗ Command '{command_text}' not found!")

if __name__ == "__main__":
    # Test các lệnh
    test_commands = ['rao', 'bot', 'hi', 'hello', 'chao', 'prefix']
    
    for cmd in test_commands:
        test_command(cmd)