#!/usr/bin/env python3
import argparse, subprocess, os, sys, threading, queue, time

def read_targets(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def run_module(target, module_cmd):
    full_cmd = f"{module_cmd} {target}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return f"--- {target} ---\n{result.stdout}{result.stderr}"

def mass_scan(target_file, module_cmd, threads=10):
    targets = read_targets(target_file)
    if not targets:
        print("No targets found.")
        return
    q = queue.Queue()
    for t in targets:
        q.put(t)
    results = []
    def worker():
        while not q.empty():
            target = q.get()
            res = run_module(target, module_cmd)
            results.append(res)
            q.task_done()
    workers = []
    for _ in range(min(threads, len(targets))):
        t = threading.Thread(target=worker)
        t.start()
        workers.append(t)
    for t in workers:
        t.join()
    print("\n".join(results))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a module against a list of targets")
    parser.add_argument("target_file", help="File with one target per line")
    parser.add_argument("--module", required=True, help="Command template (use {target} as placeholder)")
    parser.add_argument("--threads", type=int, default=10)
    args = parser.parse_args()
    if "{target}" not in args.module:
        print("Warning: module command should contain {target} placeholder")
    mass_scan(args.target_file, args.module, args.threads)
