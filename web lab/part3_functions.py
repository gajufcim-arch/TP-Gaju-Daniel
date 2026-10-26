import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def fetch(url, timeout=10):
    return requests.get(url, timeout=timeout)

print(fetch(BASE_URL).status_code)

def get_status(url: str) -> int:
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print(get_status(BASE_URL + "/"))
time.sleep(1)
print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)
print(get_status(BASE_URL + "/sitemap.xml"))

time.sleep(1)
print(fetch(BASE_URL).status_code)
time.sleep(1)
print(fetch(BASE_URL, timeout=3).status_code)

def get_title(html):
    """Returnează titlul paginii, refolosind logica de extragere."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

help(get_title)

try:
    get_status(123)
except Exception as e:
    print("Eroare la apelul cu 123:", type(e).__name__, e)

def page_exists(url):
    try:
        requests.get(url, timeout=TIMEOUT)
        return True
    except requests.RequestException:
        return False

print(page_exists("https://this-domain-does-not-exist.invalid"))

def check_paths(base, paths):
    results = {}
    for path in paths:
        time.sleep(1)
        results[path] = get_status(base + path)
    return results

print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

def get_header(url, name, default="lipsește"):
    time.sleep(1)
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)

print(get_header(BASE_URL, name="Server"))

def security_headers(url):
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    time.sleep(1)
    response = requests.get(url, timeout=TIMEOUT)
    return {header: header in response.headers for header in headers_to_check}

def score_headers(results):
    score = sum(results.values())
    total = len(results)
    return f"{score}/{total}"

print(score_headers(security_headers(BASE_URL)))

def fetch_robots(base):
    time.sleep(1)
    response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    if response.status_code == 200:
        return response.text
    return None

def disallowed_paths(robots_text):
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.startswith("Disallow:"):
            paths.append(line.split(":", 1)[1].strip())
    return paths

print(disallowed_paths(fetch_robots(BASE_URL)))

def response_times(*urls):
    times = {}
    for url in urls:
        time.sleep(1)
        start_time = time.perf_counter()
        requests.get(url, timeout=TIMEOUT)
        times[url] = time.perf_counter() - start_time
    return times

print(response_times(BASE_URL, "https://httpbin.org"))

def log(message, **details):
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    print(f"{message} | {details_str}")

log("verificat", url=BASE_URL, status=200)