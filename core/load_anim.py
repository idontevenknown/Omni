#!/usr/bin/env python3
import time, sys, os, json, random

CONFIG_PATH = os.path.expanduser("~/.omni_config")

def load_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    config[key.strip()] = val.strip()
    return config

def loading_bar(total=50, delay=0.08):
    print()
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = "█" * i + " " * (total - i)
        sys.stdout.write(f"\r   Loading... [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n   System ready.")

def loading_spinner(duration=3):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r   {spinner[i % len(spinner)]} Loading...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print("\r   ✓ Loaded.")

if __name__ == "__main__":
    config = load_config()
    style = config.get("LOADING_STYLE", "bar")
    speed = config.get("LOADING_SPEED", "normal")
    
    if speed == "fast":
        delay = 0.03
        duration = 1.5
    elif speed == "slow":
        delay = 0.15
        duration = 5
    else:  # normal
        delay = 0.08
        duration = 3
    
    if style == "spinner":
        loading_spinner(duration)
    else:
        loading_bar(50, delay)
