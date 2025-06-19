# modules/passive_enum.py

import requests
import urllib3
import re

# Disable SSL warnings globally for this module
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crtsh_enum(domain):
    print("[🔎] Searching crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for cert in data:
                name_value = cert.get("name_value")
                if name_value:
                    entries = name_value.split('\n')
                    for entry in entries:
                        if entry.endswith(domain):
                            subdomains.add(entry.strip())
            return list(subdomains)
    except Exception as e:
        print(f"[!] Error querying crt.sh: {e}")
    return []

def threatcrowd_enum(domain):
    print("[🔎] Searching ThreatCrowd...")
    url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
    try:
        # Disable SSL verification for ThreatCrowd
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("subdomains", [])
    except Exception as e:
        print(f"[!] Error querying ThreatCrowd: {e}")
    return []

def passive_enum(domain):
    subdomains = set()

    crtsh_results = crtsh_enum(domain)
    threatcrowd_results = threatcrowd_enum(domain)

    subdomains.update(crtsh_results)
    subdomains.update(threatcrowd_results)

    print(f"[✅] Passive enum found {len(subdomains)} subdomains.")
    return list(subdomains)
