#!/usr/bin/env python3
import socket, os, sys, threading, re
import argparse

def subdomains(domain, wordlist="~/Omni/wordlists/subdomains.txt"):
    found = []
    try:
        with open(os.path.expanduser(wordlist)) as f:
            subs = [line.strip() for line in f if line.strip()]
    except:
        subs = ["www","mail","ftp"]
    for sub in subs:
        try:
            ip = socket.gethostbyname(f"{sub}.{domain}")
            found.append(f"{sub}.{domain} -> {ip}")
        except:
            pass
    return found

def port_scan(target, ports="1-1024"):
    open_ports = []
    try:
        start, end = map(int, ports.split("-"))
        for port in range(start, end+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            if s.connect_ex((target, port)) == 0:
                open_ports.append(port)
            s.close()
    except:
        pass
    return open_ports

def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} -> {ip}"
    except:
        return "DNS lookup failed"

def whois(domain):
    return f"[!] WHOIS not fully implemented. Use 'whois {domain}' manually."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconnaissance tool")
    parser.add_argument("mode", choices=["subdomains","portscan","dns","whois"])
    parser.add_argument("target", help="Domain or IP")
    parser.add_argument("--ports", default="1-1024", help="Port range for scan")
    args = parser.parse_args()
    if args.mode == "subdomains":
        print(subdomains(args.target))
    elif args.mode == "portscan":
        print(port_scan(args.target, args.ports))
    elif args.mode == "dns":
        print(dns_lookup(args.target))
    elif args.mode == "whois":
        print(whois(args.target))
