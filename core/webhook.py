#!/usr/bin/env python3
import argparse, requests, json, os

CONFIG_FILE = os.path.expanduser("~/.omni_webhooks")

def load_webhooks():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_webhooks(webhooks):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(webhooks, f, indent=2)

def send_webhook(service, message, title=""):
    webhooks = load_webhooks()
    if service not in webhooks:
        return f"Error: No webhook URL configured for {service}"
    url = webhooks[service]
    if service.lower() == "discord":
        payload = {"content": message} if not title else {"content": f"**{title}**\n{message}"}
    elif service.lower() == "telegram":
        payload = {"chat_id": "@your_chat_id", "text": f"{title}\n{message}"}  # You'll need to set chat_id
    elif service.lower() == "slack":
        payload = {"text": f"*{title}*\n{message}"}
    else:
        return f"Unsupported service: {service}"
    try:
        r = requests.post(url, json=payload, timeout=10)
        return f"Sent to {service}: HTTP {r.status_code}"
    except Exception as e:
        return f"Error: {e}"

def configure_webhook(service, url):
    webhooks = load_webhooks()
    webhooks[service] = url
    save_webhooks(webhooks)
    print(f"Configured {service} webhook: {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send webhook alerts")
    parser.add_argument("mode", choices=["send", "config"])
    parser.add_argument("--service", help="discord/telegram/slack")
    parser.add_argument("--url", help="Webhook URL")
    parser.add_argument("--message", help="Message to send")
    parser.add_argument("--title", default="", help="Optional title")
    args = parser.parse_args()
    if args.mode == "config":
        if args.service and args.url:
            configure_webhook(args.service, args.url)
        else:
            print("Please provide --service and --url")
    elif args.mode == "send":
        if args.service and args.message:
            print(send_webhook(args.service, args.message, args.title))
        else:
            print("Please provide --service and --message")
