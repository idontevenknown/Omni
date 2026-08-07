#!/usr/bin/env python3
import os, sys, struct, zlib, random, argparse
from PIL import Image

def append_payload(infile, payload, outfile=None):
    if outfile is None:
        outfile = infile + "_appended"
    with open(infile, "rb") as f:
        data = f.read()
    if isinstance(payload, str):
        payload = payload.encode()
    with open(outfile, "wb") as f:
        f.write(data + payload)
    return f"Payload appended to {outfile}"

def lsb_hide(image_in, message, output=None):
    img = Image.open(image_in)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    data = list(img.getdata())
    new_data = []
    binary_message = ''.join(format(ord(c), '08b') for c in message) + '11111111'
    idx = 0
    for pixel in data:
        if idx < len(binary_message):
            r, g, b = pixel
            bit = int(binary_message[idx])
            r = (r & ~1) | bit
            idx += 1
            if idx < len(binary_message):
                bit = int(binary_message[idx])
                g = (g & ~1) | bit
                idx += 1
            if idx < len(binary_message):
                bit = int(binary_message[idx])
                b = (b & ~1) | bit
                idx += 1
            new_data.append((r, g, b))
        else:
            new_data.append(pixel)
    img2 = Image.new(img.mode, img.size)
    img2.putdata(new_data)
    if output is None:
        output = image_in + "_lsb.png"
    img2.save(output)
    return f"Message hidden in {output}"

def polyglot_jpg_zip(jpg_file, payload_zip, output=None):
    if output is None:
        output = jpg_file + "_polyglot.jpg"
    with open(jpg_file, "rb") as f:
        jpg_data = f.read()
    with open(payload_zip, "rb") as f:
        zip_data = f.read()
    idx = jpg_data.rfind(b'\xFF\xD9')
    if idx == -1:
        return "Invalid JPEG: no FF D9 marker"
    with open(output, "wb") as f:
        f.write(jpg_data)
        f.write(zip_data)
    return f"Polyglot created: {output} (open as image or unzip)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Injection/steganography")
    parser.add_argument("mode", choices=["append","lsb","polyglot"])
    parser.add_argument("infile")
    parser.add_argument("--payload")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.mode == "append":
        if args.payload:
            if os.path.isfile(args.payload):
                with open(args.payload, "rb") as f:
                    payload_data = f.read()
            else:
                payload_data = args.payload.encode()
        else:
            payload_data = input("Enter payload text: ").encode()
        print(append_payload(args.infile, payload_data, args.output))
    elif args.mode == "lsb":
        if args.payload:
            with open(args.payload, "r") as f:
                msg = f.read()
        else:
            msg = input("Enter message to hide: ")
        print(lsb_hide(args.infile, msg, args.output))
    elif args.mode == "polyglot":
        if args.payload:
            print(polyglot_jpg_zip(args.infile, args.payload, args.output))
        else:
            print("Please specify --payload for polyglot")
