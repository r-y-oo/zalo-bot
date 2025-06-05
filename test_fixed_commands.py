#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

# Test các lệnh noprefix sau khi sửa
from mitaizl import CommandHandler

# Test xem lệnh có được load đúng không
def test_simple():
    handler = CommandHandler(None)
    
    print("Commands after fix:")
    print(list(handler.auto_mitaizl.keys()))
    
    # Test một số lệnh phổ biến
    test_commands = ['rao', 'bot', 'hi', 'hello', 'system', 'prefix']
    
    for cmd in test_commands:
        if cmd in handler.auto_mitaizl:
            print(f"✓ Command '{cmd}' found!")
        else:
            print(f"✗ Command '{cmd}' not found!")

if __name__ == "__main__":
    test_simple()