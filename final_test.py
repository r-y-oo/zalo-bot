#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

from mitaizl import CommandHandler

handler = CommandHandler(None)

print("Commands available:")
print(list(handler.auto_mitaizl.keys()))

test_commands = ['rao', 'bot', 'hi', 'hello', 'system', 'prefix', 'chao', 'alo']

print("\nTesting commands:")
for cmd in test_commands:
    if cmd in handler.auto_mitaizl:
        print(f"OK: Command '{cmd}' found!")
    else:
        print(f"FAIL: Command '{cmd}' not found!")

print(f"\nTotal commands loaded: {len(handler.auto_mitaizl)}")