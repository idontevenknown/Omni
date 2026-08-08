#!/usr/bin/env python3
import argparse, subprocess, os, sys

def generate_qr(data, output):
    # Try qrencode if available
    if os.system("which qrencode >/dev/null 2>&1") == 0:
        cmd = ["qrencode", "-o", output, "-l", "M", data]
        subprocess.run(cmd)
        return f"QR code generated: {output}"
    else:
        return "qrencode not installed. Install with: pkg install qrencode"

def decode_qr(image):
    # Try zbarimg if available
    if os.system("which zbarimg >/dev/null 2>&1") == 0:
        cmd = ["zbarimg", "--raw", image]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Decoded: {result.stdout.strip()}"
        else:
            return "No QR code found or error."
    else:
        return "zbarimg not installed. Install with: pkg install zbar"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QR code generator/decoder")
    parser.add_argument("mode", choices=["generate", "decode"])
    parser.add_argument("--data", help="Data to encode")
    parser.add_argument("--output", help="Output image file (for generate)")
    parser.add_argument("--image", help="Image file to decode")
    args = parser.parse_args()
    if args.mode == "generate":
        if not args.data or not args.output:
            print("Need --data and --output")
            sys.exit(1)
        print(generate_qr(args.data, args.output))
    elif args.mode == "decode":
        if not args.image:
            print("Need --image")
            sys.exit(1)
        print(decode_qr(args.image))
