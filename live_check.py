import requests
from concurrent.futures import ThreadPoolExecutor

def check_subdomain_http(subdomain):
    urls = [f"http://{subdomain}", f"https://{subdomain}"]
    for url in urls:
        try:
            resp = requests.get(url, timeout=5, allow_redirects=True)
            return resp.status_code
        except requests.RequestException:
            continue
    return None

def check_live_subdomains(subdomains, threads=20):
    print("[🌐] Checking for live subdomains...")
    live_info = []

    def check(sub):
        status = check_subdomain_http(sub)
        if status is not None:
            return (sub, status)
        return None

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(check, subdomains)

    for result in results:
        if result:
            sub, status = result
            live_info.append({'subdomain': sub, 'status_code': status})

    print(f"[✅] {len(live_info)} live subdomains found.")
    return live_info
