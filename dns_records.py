import dns.resolver

def query_dns_records(subdomain):
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    records = {}

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(subdomain, rtype, lifetime=5)
            records[rtype] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
            records[rtype] = []

    return records
