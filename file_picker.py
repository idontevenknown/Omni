#!/usr/bin/env python3
import os

def pick_file(start_path=None):
    if start_path is None:
        start_path = os.getcwd()
    current = start_path
    while True:
        os.system('clear')
        print(f"\nCurrent: {current}")
        items = os.listdir(current)
        dirs = [d for d in items if os.path.isdir(os.path.join(current, d))]
        files = [f for f in items if os.path.isfile(os.path.join(current, f))]
        dirs.sort()
        files.sort()
        entries = []
        entries.append(("..", ".."))
        for d in dirs:
            entries.append((d + "/", d))
        for f in files:
            entries.append((f, f))
        for idx, (display, _) in enumerate(entries, 1):
            print(f"{idx}. {display}")
        print("\n[0] Cancel")
        choice = input("Enter number or full path > ").strip()
        if choice == "0":
            return None
        if os.path.isabs(choice) and os.path.exists(choice):
            if os.path.isfile(choice):
                return choice
            else:
                current = choice
                continue
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(entries):
                target = entries[idx][1]
                if target == "..":
                    current = os.path.dirname(current)
                else:
                    full = os.path.join(current, target)
                    if os.path.isdir(full):
                        current = full
                    else:
                        return full
            else:
                print("Invalid index. Press Enter to continue...")
                input()
        else:
            print("Invalid input. Press Enter to continue...")
            input()
