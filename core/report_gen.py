#!/usr/bin/env python3
import argparse, json, os, time
from datetime import datetime

def generate_html(data, title="Omni Report"):
    html = f"""<!DOCTYPE html>
<html>
<head><title>{title}</title>
<style>
body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
.container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; }}
h1 {{ color: #333; }}
pre {{ background: #eee; padding: 10px; border-left: 4px solid #007bff; }}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<pre>{json.dumps(data, indent=2)}</pre>
</div>
</body>
</html>"""
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML report from JSON data")
    parser.add_argument("--input", help="JSON file or 'last' to use last result")
    parser.add_argument("--output", default="report.html", help="Output HTML file")
    parser.add_argument("--title", default="Omni Report", help="Report title")
    args = parser.parse_args()
    data = None
    if args.input == "last":
        # Try to load from ~/Omni/data/last_result.json (we'll store it there)
        last_file = os.path.expanduser("~/Omni/data/last_result.json")
        if os.path.exists(last_file):
            with open(last_file, 'r') as f:
                data = json.load(f)
        else:
            print("No last result found.")
            sys.exit(1)
    else:
        with open(args.input, 'r') as f:
            data = json.load(f)
    html = generate_html(data, args.title)
    with open(args.output, 'w') as f:
        f.write(html)
    print(f"Report saved to {args.output}")
