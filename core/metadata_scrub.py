#!/usr/bin/env python3
import argparse, os, subprocess

def scrub_metadata(file_path, output=None):
    if output is None:
        base, ext = os.path.splitext(file_path)
        output = base + "_scrubbed" + ext
    # Use exiftool if available, else fallback to PIL (limited)
    if os.system("which exiftool >/dev/null 2>&1") == 0:
        cmd = ["exiftool", "-all=", "-overwrite_original", "-o", output, file_path]
        subprocess.run(cmd, capture_output=True)
        return f"Metadata scrubbed via exiftool: {output}"
    else:
        # Fallback: use PIL to strip EXIF
        try:
            from PIL import Image
            img = Image.open(file_path)
            # Save without EXIF
            img.save(output, format=img.format, quality=95, optimize=True)
            return f"Metadata scrubbed via PIL: {output}"
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Strip metadata from files")
    parser.add_argument("file", help="File to scrub")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()
    print(scrub_metadata(args.file, args.output))
