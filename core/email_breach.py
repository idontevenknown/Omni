#!/usr/bin/env python3
import argparse, requests

def check_breach(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'User-Agent': 'Omni-Toolkit'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return f"[!] Email breached in {len(data)} sites: " + ', '.join([b['Name'] for b in data])
        elif r.status_code == 404:
            return "[+] No breaches found."
        else:
            return f"[-] API error: {r.status_code}"
    except:
        return "[-] Request failed (no internet?)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if email is in data breaches")
    parser.add_argument("email", help="Email address to check")
    args = parser.parse_args()
    print(check_breach(args.email))
