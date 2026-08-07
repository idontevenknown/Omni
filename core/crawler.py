#!/usr/bin/env python3
import requests, re, urllib.parse, argparse

def crawl(url, depth=1):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        resp = requests.get(url, timeout=10)
        html = resp.text
        links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
        full_links = [urllib.parse.urljoin(url, l) for l in links]
        return {"links": full_links, "emails": list(set(emails))}
    except:
        return {"error": "Crawl failed"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument("url")
    parser.add_argument("--depth", type=int, default=1)
    args = parser.parse_args()
    print(crawl(args.url, args.depth))
