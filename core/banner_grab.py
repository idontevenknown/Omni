#!/usr/bin/env python3
import argparse, socket, sys

def grab_banner(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        # Send a generic probe (HTTP HEAD if port 80/443, else a simple newline)
        if port in [80, 443, 8080, 8443]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        else:
            s.send(b"\r\n")
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner if banner else "(empty response)"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grab service banners from open ports")
    parser.add_argument("host", help="Target host (IP or domain)")
    parser.add_argument("port", type=int, help="Port number")
    args = parser.parse_args()
    banner = grab_banner(args.host, args.port)
    print(f"Banner on {args.host}:{args.port} -> {banner}")
