#!/usr/bin/env python3
import argparse, requests, json

def scrape_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return f"Error: HTTP {r.status_code}"
        data = r.json()
        subs = set()
        for entry in data:
            name = entry.get('name_value', '')
            if name:
                for n in name.split('\n'):
                    n = n.strip()
                    if n and '*' not in n:
                        subs.add(n)
        return sorted(subs)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape subdomains from crt.sh")
    parser.add_argument("domain", help="Domain to search (e.g., example.com)")
    args = parser.parse_args()
    results = scrape_subdomains(args.domain)
    if isinstance(results, list):
        for r in results:
            print(r)
    else:
        print(results)
