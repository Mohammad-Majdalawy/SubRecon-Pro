# modules/takeover_check.py

import socket
import dns.resolver

# Known vulnerable services for potential takeovers
VULNERABLE_CNAME_SIGNATURES = {
    's3.amazonaws.com': 'Amazon S3',
    'github.io': 'GitHub Pages',
    'herokudns.com': 'Heroku',
    'cloudapp.net': 'Azure',
    'bitbucket.io': 'Bitbucket',
    'unbouncepages.com': 'Unbounce',
    'readthedocs.io': 'ReadTheDocs',
    'surge.sh': 'Surge.sh',
    'wordpress.com': 'WordPress',
    'cargo.site': 'Cargo',
}

def get_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            return str(rdata.target).rstrip('.')
    except:
        return None

def detect_takeovers(subdomains):
    print("[🔐] Checking for subdomain takeover candidates...")
    vulnerable = []

    for sub in subdomains:
        cname = get_cname(sub)
        if cname:
            for signature in VULNERABLE_CNAME_SIGNATURES:
                if signature in cname:
                    print(f"[⚠️] Possible takeover: {sub} → {cname}")
                    vulnerable.append({'subdomain': sub, 'cname': cname})
                    break

    print(f"[✅] {len(vulnerable)} potential takeovers found.")
    return vulnerable
