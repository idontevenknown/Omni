#!/usr/bin/env python3
import argparse, time, schedule, subprocess, json, os, sys

CONFIG_FILE = os.path.expanduser("~/.omni_tasks")

def load_tasks():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(name, command, interval, unit):
    tasks = load_tasks()
    tasks.append({"name": name, "command": command, "interval": interval, "unit": unit})
    save_tasks(tasks)
    print(f"Task '{name}' added.")

def run_task(command):
    print(f"\n[Scheduler] Running: {command}")
    subprocess.run(command, shell=True)

def start_scheduler():
    tasks = load_tasks()
    if not tasks:
        print("No tasks configured. Use add_task first.")
        return
    for task in tasks:
        if task['unit'] == 'minutes':
            schedule.every(task['interval']).minutes.do(run_task, task['command'])
        elif task['unit'] == 'hours':
            schedule.every(task['interval']).hours.do(run_task, task['command'])
        elif task['unit'] == 'days':
            schedule.every(task['interval']).days.do(run_task, task['command'])
        else:
            print(f"Unknown unit: {task['unit']} for task {task['name']}")
    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task scheduler for periodic scans")
    parser.add_argument("mode", choices=["add", "start", "list"])
    parser.add_argument("--name", help="Task name")
    parser.add_argument("--command", help="Command to run")
    parser.add_argument("--interval", type=int, help="Interval value")
    parser.add_argument("--unit", choices=["minutes", "hours", "days"], help="Interval unit")
    args = parser.parse_args()
    if args.mode == "add":
        if args.name and args.command and args.interval and args.unit:
            add_task(args.name, args.command, args.interval, args.unit)
        else:
            print("Missing arguments for add")
    elif args.mode == "start":
        start_scheduler()
    elif args.mode == "list":
        tasks = load_tasks()
        if tasks:
            for t in tasks:
                print(f"{t['name']}: {t['command']} every {t['interval']} {t['unit']}")
        else:
            print("No tasks.")
