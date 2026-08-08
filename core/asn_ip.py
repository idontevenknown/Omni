#!/usr/bin/env python3
import argparse, requests, json

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"Error: HTTP {r.status_code}"
        data = r.json()
        if data['status'] == 'fail':
            return f"Error: {data.get('message', 'Unknown')}"
        return {
            'IP': data['query'],
            'ISP': data['isp'],
            'Organization': data['org'],
            'ASN': data['as'],
            'Country': data['country'],
            'City': data['city'],
            'Region': data['regionName'],
            'Timezone': data['timezone']
        }
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get IP intelligence (ASN, ISP, etc.)")
    parser.add_argument("ip", help="IP address")
    args = parser.parse_args()
    info = get_ip_info(args.ip)
    if isinstance(info, dict):
        for k, v in info.items():
            print(f"{k}: {v}")
    else:
        print(info)
