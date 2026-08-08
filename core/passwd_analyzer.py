#!/usr/bin/env python3
import argparse, math, string, re

def entropy(password):
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset_size += 32
    if charset_size == 0: return 0
    return len(password) * math.log2(charset_size)

def crack_time(ent):
    # seconds for 1e9 guesses/sec (very rough)
    sec = 2 ** ent / 1e9
    if sec < 60: return f"{sec:.1f} seconds"
    if sec < 3600: return f"{sec/60:.1f} minutes"
    if sec < 86400: return f"{sec/3600:.1f} hours"
    if sec < 31536000: return f"{sec/86400:.1f} days"
    return f"{sec/31536000:.1f} years"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze password strength")
    parser.add_argument("password", help="Password to analyze")
    args = parser.parse_args()
    ent = entropy(args.password)
    print(f"Length: {len(args.password)}")
    print(f"Entropy: {ent:.1f} bits")
    print(f"Estimated crack time (1e9 guesses/s): {crack_time(ent)}")
