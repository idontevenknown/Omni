#!/usr/bin/env python3
import os, sys, datetime
from colorama import init, Fore, Style
init(autoreset=True)

CONFIG_PATH = os.path.expanduser("~/.omni_config")
THEMES_PATH = os.path.expanduser("~/Omni/core/themes.py")

USER_NAME = "OVERSEER"
GREETING = "Welcome back"
THEME = "default"

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                if key == "USER_NAME": USER_NAME = val.strip()
                elif key == "GREETING": GREETING = val.strip()
                elif key == "THEME": THEME = val.strip()

if os.path.exists(THEMES_PATH):
    import importlib.util
    spec = importlib.util.spec_from_file_location("themes", THEMES_PATH)
    themes_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(themes_mod)
    theme_colors = themes_mod.themes.get(THEME, themes_mod.themes.get("default"))
else:
    theme_colors = {"banner": Fore.CYAN, "greeting": Fore.MAGENTA}

# Massive centered ASCII art – 15 lines, 60 chars wide, centered in 80 columns
banner_lines = [
    "   ██████  ██    ██ ███████ ██████  ███████ ███████ ██████  ",
    "  ██    ██ ██    ██ ██      ██   ██ ██      ██      ██   ██ ",
    "  ██    ██ ██    ██ █████   ██████  █████   █████   ██████  ",
    "  ██    ██ ██    ██ ██      ██   ██ ██      ██      ██   ██ ",
    "   ██████   ██████  ███████ ██   ██ ███████ ███████ ██   ██ ",
    "",
    "   ██████  ███████ ███████ ███████ ██████  ███████ ██████  ",
    "  ██   ██ ██      ██      ██      ██   ██ ██      ██   ██ ",
    "  ██████  █████   █████   █████   ██████  █████   ██████   ",
    "  ██   ██ ██      ██      ██      ██   ██ ██      ██   ██ ",
    "  ██   ██ ███████ ███████ ███████ ██   ██ ███████ ██   ██ ",
]

# Center each line in an 80‑column terminal (we'll pad with spaces)
width = 80
centered = []
for line in banner_lines:
    padding = max(0, (width - len(line)) // 2)
    centered.append(" " * padding + line)

banner = "\n".join(centered)

now = datetime.datetime.now()
hour = now.hour
if hour < 12:    time_greeting = "Good morning"
elif hour < 18: time_greeting = "Good afternoon"
else:           time_greeting = "Good evening"
current_time = now.strftime("%I:%M %p")

print(theme_colors["banner"] + banner + Style.RESET_ALL)
print(theme_colors["greeting"] + f"   {time_greeting}, {USER_NAME} – {current_time}" + Style.RESET_ALL)
print()
