#!/usr/bin/env python3
import argparse, socket, dns.resolver, json

# Simplified list of known takeover patterns (CNAME to cloud services)
TAKEOVER_PATTERNS = {
    'github.io': 'GitHub Pages',
    'herokuapp.com': 'Heroku',
    'amazonaws.com': 'AWS S3',
    'cloudfront.net': 'AWS CloudFront',
    'azurewebsites.net': 'Azure',
    'netlify.app': 'Netlify',
    'vercel.app': 'Vercel',
    'firebaseapp.com': 'Firebase',
    'bitbucket.io': 'Bitbucket',
}

def check_takeover(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        for rdata in answers:
            cname = str(rdata.target).rstrip('.')
            for pattern, service in TAKEOVER_PATTERNS.items():
                if pattern in cname:
                    return f"[!] Potential takeover! {domain} -> {cname} (unclaimed {service})"
        return f"[-] No takeover detected for {domain}"
    except:
        return f"[-] No CNAME record or lookup failed for {domain}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check subdomain takeover")
    parser.add_argument("domain", help="Subdomain to check (e.g., test.example.com)")
    args = parser.parse_args()
    print(check_takeover(args.domain))
