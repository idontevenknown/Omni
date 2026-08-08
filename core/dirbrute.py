#!/usr/bin/env python3
import argparse, requests, threading, queue, os

def brute(url, wordlist, threads=10):
    q = queue.Queue()
    with open(wordlist, 'r') as f:
        for line in f:
            q.put(line.strip())
    found = []
    def worker():
        while not q.empty():
            word = q.get()
            target = url.rstrip('/') + '/' + word
            try:
                r = requests.get(target, timeout=5)
                if r.status_code in [200, 301, 302, 403, 401]:
                    found.append(f"{target} -> {r.status_code}")
            except:
                pass
            q.task_done()
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()
    q.join()
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory brute-forcer")
    parser.add_argument("url", help="Base URL (e.g., https://example.com)")
    parser.add_argument("--wordlist", default="~/Omni/wordlists/dirlist.txt")
    parser.add_argument("--threads", type=int, default=10)
    args = parser.parse_args()
    wl = os.path.expanduser(args.wordlist)
    if not os.path.exists(wl):
        print("Wordlist not found. Creating a small default list...")
        with open(wl, 'w') as f:
            f.write('\n'.join(['admin','login','wp-admin','backup','uploads','config','.git','.env','secret','api']))
    results = brute(args.url, wl, args.threads)
    for r in results:
        print(r)
