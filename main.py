import argparse
from modules.passive_enum import passive_enum
from modules.brute_force import brute_force_enum
from modules.live_check import check_live_subdomains
from modules.takeover_check import detect_takeovers
from modules.report_generator import generate_report
from modules.dns_records import query_dns_records

def main():
    parser = argparse.ArgumentParser(description="🔍 SubRecon Pro - Advanced Subdomain Enumerator")
    parser.add_argument('--domain', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('--output', choices=['json', 'html'], default='html', help='Report format')
    parser.add_argument('--brute', action='store_true', help='Enable brute-force enumeration')
    parser.add_argument('--wordlist', help='Path to subdomain wordlist file for brute forcing')

    args = parser.parse_args()
    domain = args.domain

    print(f"🔍 Enumerating subdomains for: {domain}")

    # 1. Passive Enumeration
    passive_results = passive_enum(domain)

    # 2. Brute Force Enumeration (optional)
    if args.brute:
        wordlist_path = args.wordlist if args.wordlist else 'wordlists/subdomains.txt'
        brute_results = brute_force_enum(domain, wordlist_path)
    else:
        brute_results = []

    # Merge and deduplicate subdomains
    all_subdomains = sorted(set(passive_results + brute_results))

    # 3. Check live subdomains (with status codes)
    live_subdomains_info = check_live_subdomains(all_subdomains)
    live_subdomains = [info['subdomain'] for info in live_subdomains_info]

    # 4. Detect takeover vulnerabilities
    takeover_vulns = detect_takeovers(live_subdomains)

    # 5. DNS Records Gathering
    print("[🗂] Gathering DNS records for discovered subdomains...")
    dns_info = {}
    for sub in all_subdomains:
        dns_info[sub] = query_dns_records(sub)

    # 6. Generate report (html/json)
    generate_report(domain, all_subdomains, live_subdomains_info, takeover_vulns, args.output, dns_info)

    print("✅ Enumeration complete!")

if __name__ == '__main__':
    main()
