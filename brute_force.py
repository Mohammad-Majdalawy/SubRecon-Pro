# modules/brute_force.py

import socket
from concurrent.futures import ThreadPoolExecutor

def load_wordlist(filepath='wordlists/subdomains.txt'):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {filepath}")
        return []

def resolve_subdomain(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return subdomain
    except socket.gaierror:
        return None

def brute_force_enum(domain, wordlist_path='wordlists/subdomains.txt', threads=20):
    print("[⚙️] Starting brute-force enumeration...")
    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        print("[!] No subdomains to brute force.")
        return []

    subdomains = [f"{word}.{domain}" for word in wordlist]

    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(resolve_subdomain, sub) for sub in subdomains]
        for future in futures:
            result = future.result()
            if result:
                print(f"[+] Found: {result}")
                results.append(result)

    print(f"[✅] Brute-force found {len(results)} subdomains.")
    return results
