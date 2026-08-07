#!/usr/bin/env python3
import hashlib, os, math, argparse
from PIL import Image, ExifTags

def hash_file(filepath, algo="sha256"):
    try:
        hash_func = hashlib.new(algo)
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return f"{algo}: {hash_func.hexdigest()}"
    except:
        return "Error reading file"

def entropy(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        if not data:
            return 0.0
        freq = {}
        for b in data:
            freq[b] = freq.get(b, 0) + 1
        ent = -sum((c/len(data)) * math.log2(c/len(data)) for c in freq.values())
        return round(ent, 4)
    except:
        return -1

def exif_read(filepath):
    try:
        img = Image.open(filepath)
        exif = img._getexif()
        if not exif:
            return "No EXIF data found."
        result = {}
        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            result[tag] = value
        return result
    except Exception as e:
        return f"Error: {e}"

def exif_write(filepath, tag, value, output=None):
    try:
        img = Image.open(filepath)
        exif = img.getexif()
        if isinstance(tag, str):
            for k, v in ExifTags.TAGS.items():
                if v == tag:
                    tag = k
                    break
            else:
                return f"Tag '{tag}' not found."
        exif[tag] = value
        if output is None:
            output = filepath + "_exif.jpg"
        img.save(output, exif=exif)
        return f"EXIF written to {output}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File forensics")
    parser.add_argument("mode", choices=["hash","entropy","exif_read","exif_write"])
    parser.add_argument("file")
    parser.add_argument("--algo", default="sha256")
    parser.add_argument("--tag")
    parser.add_argument("--value")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.mode == "hash":
        print(hash_file(args.file, args.algo))
    elif args.mode == "entropy":
        print(entropy(args.file))
    elif args.mode == "exif_read":
        print(exif_read(args.file))
    elif args.mode == "exif_write":
        if args.tag and args.value:
            print(exif_write(args.file, args.tag, args.value, args.output))
        else:
            print("Please provide --tag and --value")
