#!/usr/bin/env python3
import os

CONFIG_PATH = os.path.expanduser("~/.omni_config")

def get_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, val = line.strip().split('=', 1)
                        config[key.strip()] = val.strip()
    return config

def set_config(key, value):
    config = get_config()
    config[key] = value
    lines = []
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            lines = f.readlines()
    # Remove existing line for the key
    new_lines = []
    for line in lines:
        if line.strip() and not line.startswith('#') and line.split('=')[0].strip() == key:
            continue
        new_lines.append(line)
    # Add the new line
    new_lines.append(f"{key}={value}\n")
    with open(CONFIG_PATH, 'w') as f:
        f.writelines(new_lines)
    print(f"✅ {key} updated to: {value}")
