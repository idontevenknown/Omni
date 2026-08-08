#!/usr/bin/env python3
import argparse, random, json

# Simplified fake data pools
FIRST_NAMES = ["John","Jane","Michael","Sarah","David","Emma","Chris","Jessica","Daniel","Laura"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
CITIES = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","Austin"]
STREETS = ["Main St","Oak Ave","Maple Rd","Elm Blvd","Pine Ln","Cedar Dr","Birch Way","Willow Ct","Spruce St","Ash Ave"]
DOMAINS = ["gmail.com","yahoo.com","outlook.com","hotmail.com","protonmail.com"]
SSN_PREFIX = ["000","111","222","333","444","555","666","777","888","999"]

def generate_identity():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    dob = f"{random.randint(1,12)}/{random.randint(1,28)}/{random.randint(1960,2005)}"
    address = f"{random.randint(100,9999)} {random.choice(STREETS)}, {random.choice(CITIES)}"
    email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@{random.choice(DOMAINS)}"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    ssn = f"{random.choice(SSN_PREFIX)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    return {
        "First Name": first,
        "Last Name": last,
        "Date of Birth": dob,
        "Address": address,
        "Email": email,
        "Phone": phone,
        "SSN": ssn
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake identities")
    parser.add_argument("--count", type=int, default=1, help="Number of identities")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    identities = [generate_identity() for _ in range(args.count)]
    if args.json:
        print(json.dumps(identities, indent=2))
    else:
        for i, id in enumerate(identities, 1):
            print(f"--- Identity {i} ---")
            for k, v in id.items():
                print(f"{k}: {v}")
