#!/usr/bin/env python3
import argparse, subprocess, re, json

def analyze_ssl(host, port=443):
    try:
        cmd = ["openssl", "s_client", "-connect", f"{host}:{port}", "-servername", host, "-tlsextdebug", "-status"]
        proc = subprocess.run(cmd, input=b"\n", capture_output=True, text=True, timeout=10)
        output = proc.stdout
        # Extract certificate info
        cert_re = re.search(r"subject=(.*?)\n", output)
        issuer_re = re.search(r"issuer=(.*?)\n", output)
        not_before = re.search(r"notBefore=(.*?)\n", output)
        not_after = re.search(r"notAfter=(.*?)\n", output)
        cipher = re.search(r"New, (.*?), Cipher is (.*?)\n", output)
        result = {}
        if cert_re:
            result['Subject'] = cert_re.group(1).strip()
        if issuer_re:
            result['Issuer'] = issuer_re.group(1).strip()
        if not_before:
            result['Not Before'] = not_before.group(1).strip()
        if not_after:
            result['Not After'] = not_after.group(1).strip()
        if cipher:
            result['Cipher'] = cipher.group(2).strip()
        if not result:
            return "No SSL data retrieved (maybe openssl not installed or target not responding)"
        return result
    except subprocess.TimeoutExpired:
        return "Connection timeout"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze SSL/TLS certificate")
    parser.add_argument("host", help="Target host (domain)")
    parser.add_argument("--port", type=int, default=443, help="Port (default 443)")
    args = parser.parse_args()
    result = analyze_ssl(args.host, args.port)
    if isinstance(result, dict):
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print(result)
