#!/usr/bin/env python3
import argparse, itertools, os

def leetspeak(word):
    subs = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7','g':'9'}
    return ''.join(subs.get(c.lower(), c) for c in word)

def generate_wordlist(first, last, middle, year, nicknames, fav_words):
    words = set()
    parts = [first, last, middle] if middle else [first, last]
    # First+Last combos
    for a, b in itertools.permutations(parts, 2):
        words.add(a+b)
        words.add(a+'.'+b)
        words.add(a+'_'+b)
        words.add(a+b+year)
        words.add(a+year+b)
        words.add(year+a+b)
        words.add(a+year)
        words.add(b+year)
        words.add(a+b+'123')
        words.add(a+b+'!')
    # Leetspeak
    for w in list(words):
        words.add(leetspeak(w))
    # Nicknames
    for n in nicknames:
        words.add(n)
        words.add(n+year)
    # Favorite words
    for fw in fav_words:
        words.add(fw)
        words.add(fw+year)
    return sorted(words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate custom wordlists")
    parser.add_argument("--first", required=True)
    parser.add_argument("--last", required=True)
    parser.add_argument("--middle", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--nick", nargs="*", default=[])
    parser.add_argument("--words", nargs="*", default=[], help="Favorite words")
    parser.add_argument("--output", default="wordlist.txt")
    args = parser.parse_args()
    wl = generate_wordlist(args.first, args.last, args.middle, args.year, args.nick, args.words)
    with open(args.output, 'w') as f:
        f.write('\n'.join(wl))
    print(f"Generated {len(wl)} words -> {args.output}")
