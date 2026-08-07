#!/usr/bin/env python3
import subprocess, os, socket, threading, ipaddress, argparse

def arp_scan(interface=None):
    if os.system("which arp-scan >/dev/null 2>&1") == 0:
        cmd = ["arp-scan", "--localnet"] if not interface else ["arp-scan", "-I", interface]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    else:
        return "arp-scan not installed. Install with: pkg install arp-scan"

def ping_sweep(cidr):
    net = ipaddress.ip_network(cidr, strict=False)
    alive = []
    def ping(ip):
        if os.system(f"ping -c 1 -W 1 {ip} >/dev/null 2>&1") == 0:
            alive.append(str(ip))
    threads = []
    for ip in net.hosts():
        t = threading.Thread(target=ping, args=(ip,))
        t.start()
        threads.append(t)
        if len(threads) > 50:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return alive

def local_ports():
    result = subprocess.run("netstat -tulpn 2>/dev/null", shell=True, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument("mode", choices=["arp","ping","ports"])
    parser.add_argument("--interface", default=None)
    parser.add_argument("--cidr")
    args = parser.parse_args()
    if args.mode == "arp":
        print(arp_scan(args.interface))
    elif args.mode == "ping":
        if args.cidr:
            print(ping_sweep(args.cidr))
        else:
            print("Please specify --cidr")
    elif args.mode == "ports":
        print(local_ports())
