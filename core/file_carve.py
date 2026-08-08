#!/usr/bin/env python3
import argparse, subprocess, os

def carve_image(image_file, output_dir="carved"):
    if os.system("which foremost >/dev/null 2>&1") != 0:
        return "foremost is not installed. Install with: pkg install foremost"
    os.makedirs(output_dir, exist_ok=True)
    cmd = ["foremost", "-i", image_file, "-o", output_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return f"Carving completed. Files saved to {output_dir}"
    else:
        return f"Error: {result.stderr}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carve files from a disk image")
    parser.add_argument("image", help="Raw image file (e.g., .dd, .img)")
    parser.add_argument("--output", default="carved", help="Output directory")
    args = parser.parse_args()
    print(carve_image(args.image, args.output))
