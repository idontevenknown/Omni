#!/usr/bin/env python3
import argparse, hashlib, os

def crack_hash(hash_value, hash_type, wordlist):
    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if hash_type == 'md5':
                    h = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == 'sha1':
                    h = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == 'sha256':
                    h = hashlib.sha256(word.encode()).hexdigest()
                else:
                    return "Unsupported hash type."
                if h == hash_value:
                    return f"Found: {word}"
        return "Not found in wordlist."
    except FileNotFoundError:
        return "Wordlist not found."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline hash cracker (dictionary)")
    parser.add_argument("hash", help="Hash value")
    parser.add_argument("--type", choices=["md5","sha1","sha256"], default="md5")
    parser.add_argument("--wordlist", default="~/Omni/wordlists/rockyou.txt")
    args = parser.parse_args()
    wl = os.path.expanduser(args.wordlist)
    if not os.path.exists(wl):
        print("Wordlist not found. Creating small sample list...")
        with open(wl, 'w') as f:
            f.write('\n'.join(['password','123456','admin','letmein','qwerty','abc123']))
    print(crack_hash(args.hash, args.type, wl))
