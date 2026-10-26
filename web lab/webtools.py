import requests
import time
import socket
import ssl
import urllib.parse
import re
import json

TIMEOUT = 10


DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}

def fetch(url, timeout=TIMEOUT):
    """Returnează obiectul răspuns pentru un URL."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)

def get_status(url):
    """Returnează codul de stare HTTP pentru adresa URL."""
    return fetch(url).status_code

def get_title(html):
    """Extrage și returnează titlul din codul HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "Lipsește"

def security_headers(url):
    """Verifică prezența a cinci antete de securitate."""
    headers_to_check = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    time.sleep(1)
    response = fetch(url)
    return {header: header in response.headers for header in headers_to_check}

def score_headers(results):
    """Calculează scorul antetelor de securitate (ex: 3/5)."""
    return f"{sum(results.values())}/{len(results)}"

def check_paths(base, paths):
    """Verifică statusul pentru o listă de căi relative."""
    results = {}
    for path in paths:
        time.sleep(1)
        results[path] = get_status(urllib.parse.urljoin(base, path))
    return results

def resolve(hostname):
    """Returnează adresa IP a domeniului."""
    return socket.gethostbyname(hostname)

def cert_days_left(hostname):
    """Calculează zilele rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
            return int((expire_timestamp - time.time()) / 86400)

def extract_links(html):
    """Extrage toate legăturile (href) din HTML, fără duplicate."""
    return list(set(re.findall(r'href="([^"]+)"', html)))

def split_links(links, domain):
    """Separă legăturile în interne și externe comparând domeniul."""
    internal, external = [], []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)
    return internal, external

def fetch_robots(base):
    """Descarcă fișierul robots.txt."""
    time.sleep(1)
    resp = fetch(base + "/robots.txt")
    return resp.text if resp.status_code == 200 else None

def disallowed_paths(robots_text):
    """Returnează lista căilor interzise (Disallow) din robots.txt."""
    if not robots_text: 
        return []
    return [line.split(":", 1)[1].strip() for line in robots_text.splitlines() if line.startswith("Disallow:")]


def site_report(url):
    """Generează, afișează și salvează un raport complet al site-ului."""
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    base_url = f"{parsed_url.scheme}://{domain}"

    time.sleep(1)
    resp = fetch(url)
    
    time.sleep(1)
    http_resp = requests.get(f"http://{domain}", timeout=TIMEOUT, headers=DEFAULT_HEADERS)
    if http_resp.history:
        redirects = " -> ".join([f"{r.status_code} {r.url}" for r in http_resp.history] + [http_resp.url])
    else:
        redirects = http_resp.url

    internal_links, external_links = split_links(extract_links(resp.text), domain)
    disallowed = disallowed_paths(fetch_robots(base_url))

    report_data = {
        "Raport site": url,
        "Cod de stare": resp.status_code,
        "Titlu": get_title(resp.text),
        "Adresa IP": resolve(domain),
        "Redirectionari": redirects,
        "Scor securitate": score_headers(security_headers(url)),
        "Certificat": f"{cert_days_left(domain)} de zile ramase",
        "Legaturi": f"{len(internal_links)} interne, {len(external_links)} externe",
        "Cai interzise": ", ".join(disallowed) if disallowed else "Niciuna"
    }

    print(f"=== Raport site: {url} ===")
    for key, value in report_data.items():
        if key != "Raport site":
            print(f"{key}:\t{value}")
    print("Salvat în report.json")

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    
    print("Autotest:", get_status("https://cybercor.org"))