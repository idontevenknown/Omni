#!/usr/bin/env python3
import json, csv, os, time, argparse

def export_json(data, filename=None):
    if not filename:
        filename = f"data/export_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return filename

def export_csv(data, filename=None):
    if not data:
        return None
    if not filename:
        filename = f"data/export_{int(time.time())}.csv"
    keys = data[0].keys() if isinstance(data, list) and data else data.keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export data")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--file")
    args = parser.parse_args()
    print("Export module is meant to be used via menu or import.")
