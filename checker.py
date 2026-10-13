# Autor: Gaju Daniel
# Grupa: SI-264


import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

TIMEOUT = 5  


def _short_error(exc):
    """Transformă o excepție requests într-un mesaj scurt."""
    if isinstance(exc, requests.exceptions.Timeout):
        return "timeout"
    if isinstance(exc, requests.exceptions.ConnectionError):
        return "eroare de conexiune"
    return type(exc).__name__


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return "https://" + host.strip("/") + "/" + path.lstrip("/")


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.lower().startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as exc:
        print("Eroare:", _short_error(exc))
        return
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as exc:
        return {"status": None, "error": _short_error(exc)}

    
    content_type = response.headers.get("Content-Type", "")
    content_type = content_type.split(";")[0].strip()

    return {
        "status": response.status_code,
        "content_type": content_type,
        "length": len(response.content),
        "server": response.headers.get("Server", "unknown"),
    }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        results.append((url, check_site(url)))

    working = [(url, r) for url, r in results if r["status"] == 200]
    working.sort(key=lambda item: item[1]["length"], reverse=True)

    for url, r in working:
        print(f"{url} -> {r['status']}, {r['length']} octeți")

    ok = len(working)
    failed = len(results) - ok
    print(f"Reușite: {ok} | Eșuate: {failed}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as exc:
        return {"status": None, "error": _short_error(exc)}

    present = []
    missing = []
    for header in SECURITY_HEADERS:  
        
        if header in response.headers:
            present.append(header)
        else:
            missing.append(header)

    score = len(present) * 100 // len(SECURITY_HEADERS)
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None
    last_error = None
    made = 0

    while made < attempts:
        made += 1  
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as exc:
            last_error = _short_error(exc)
            continue

        status = response.status_code
        last_error = None
        if status < 500:
            break  

    result = {"status": status, "attempts": made}
    if status is None and last_error is not None:
        result["error"] = last_error
    return result
