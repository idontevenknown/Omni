#!/usr/bin/env python3
import argparse, os, random, string, json

DECOY_EXTENSIONS = [".docx", ".pdf", ".xlsx", ".txt", ".zip", ".sql"]
DECOY_NAMES = ["passwords", "accounts", "bank_transactions", "customers", "employees", "secrets", "backup", "config", "database", "keys"]

def generate_decoy(output_path, size_kb=10):
    # Create a file with random gibberish
    size_bytes = size_kb * 1024
    content = ''.join(random.choices(string.ascii_letters + string.digits + ' \n\t', k=size_bytes))
    with open(output_path, 'w') as f:
        f.write(content)
    return f"Decoy file created: {output_path} ({size_kb} KB)"

def generate_multiple(count, folder):
    os.makedirs(folder, exist_ok=True)
    created = []
    for _ in range(count):
        name = random.choice(DECOY_NAMES) + str(random.randint(1,999)) + random.choice(DECOY_EXTENSIONS)
        path = os.path.join(folder, name)
        size = random.randint(5, 50)
        generate_decoy(path, size)
        created.append(path)
    return f"Generated {count} decoy files in {folder}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate decoy files for bait")
    parser.add_argument("--output", help="Single output file path")
    parser.add_argument("--size", type=int, default=10, help="Size in KB (default 10)")
    parser.add_argument("--count", type=int, help="Number of decoy files to generate")
    parser.add_argument("--folder", help="Folder to save multiple files")
    args = parser.parse_args()
    if args.count and args.folder:
        print(generate_multiple(args.count, args.folder))
    elif args.output:
        print(generate_decoy(args.output, args.size))
    else:
        print("Please provide either --output or both --count and --folder")
