#!/usr/bin/env python3
import argparse, socket

def reverse_lookup(ip):
    try:
        host = socket.gethostbyaddr(ip)
        return f"{ip} -> {host[0]}"
    except socket.herror:
        return f"{ip} -> No PTR record found"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse DNS lookup (PTR)")
    parser.add_argument("ip", help="IP address")
    args = parser.parse_args()
    print(reverse_lookup(args.ip))
