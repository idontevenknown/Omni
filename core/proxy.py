#!/usr/bin/env python3
import os, argparse, json

CONFIG_FILE = os.path.expanduser("~/.omni_proxy")

def load_proxy():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"http": "", "https": "", "tor": False}

def save_proxy(proxy_dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(proxy_dict, f, indent=2)

def set_proxy(http, https):
    cfg = load_proxy()
    cfg['http'] = http
    cfg['https'] = https
    save_proxy(cfg)
    print(f"Proxy set: HTTP={http}, HTTPS={https}")

def unset_proxy():
    cfg = load_proxy()
    cfg['http'] = ""
    cfg['https'] = ""
    save_proxy(cfg)
    print("Proxy unset")

def toggle_tor():
    cfg = load_proxy()
    cfg['tor'] = not cfg.get('tor', False)
    save_proxy(cfg)
    print(f"Tor mode: {'ON' if cfg['tor'] else 'OFF'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy & Tor support")
    parser.add_argument("mode", choices=["set", "unset", "tor"])
    parser.add_argument("--http", help="HTTP proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--https", help="HTTPS proxy")
    args = parser.parse_args()
    if args.mode == "set":
        set_proxy(args.http or "", args.https or "")
    elif args.mode == "unset":
        unset_proxy()
    elif args.mode == "tor":
        toggle_tor()
