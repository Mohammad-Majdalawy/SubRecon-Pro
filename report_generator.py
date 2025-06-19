import os
import json
from jinja2 import Environment, FileSystemLoader

def generate_report(domain, all_subdomains, live_subdomains_info, takeovers, format='html', dns_info=None):
    os.makedirs('output/reports', exist_ok=True)
    filename = f"output/reports/{domain.replace('.', '_')}_report.{format}"

    if format == 'json':
        report_data = {
            "domain": domain,
            "total_discovered": len(all_subdomains),
            "live_subdomains": live_subdomains_info,
            "potential_takeovers": takeovers,
            "dns_records": dns_info
        }
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=4)
        print(f"[📄] JSON report saved to: {filename}")

    elif format == 'html':
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('report_template.html')
            html_content = template.render(
                domain=domain,
                all=all_subdomains,
                live=live_subdomains_info,
                takeovers=takeovers,
                dns_info=dns_info
            )
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"[📄] HTML report saved to: {filename}")
        except Exception as e:
            print(f"[❌] Failed to generate HTML report: {e}")

    else:
        print(f"[!] Unsupported report format: {format}")
