#!/usr/bin/env python3
import argparse
from PIL import Image

def detect_lsb(image_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        data = list(img.getdata())
        # Check if LSBs are random (entropy based)
        import math
        lsb_sequence = []
        for pixel in data[:10000]:  # sample first 10000 pixels
            r, g, b = pixel
            lsb_sequence.append(r & 1)
            lsb_sequence.append(g & 1)
            lsb_sequence.append(b & 1)
        # Calculate entropy of LSBs
        if not lsb_sequence:
            return "No data sampled."
        freq = [0, 0]
        for bit in lsb_sequence:
            freq[bit] += 1
        total = len(lsb_sequence)
        p0 = freq[0] / total
        p1 = freq[1] / total
        if p0 == 0 or p1 == 0:
            return "LSB seems uniform (likely no hidden data)."
        entropy = - (p0 * math.log2(p0) + p1 * math.log2(p1))
        if entropy > 0.9:
            return f"Suspicious: LSB entropy is {entropy:.2f} (potential hidden data)."
        else:
            return f"Normal: LSB entropy is {entropy:.2f} (likely no hidden data)."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect LSB steganography in images")
    parser.add_argument("image", help="Image file path")
    args = parser.parse_args()
    print(detect_lsb(args.image))
