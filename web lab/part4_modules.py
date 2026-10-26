import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

parsed_url = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print(parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.query, parsed_url.fragment)

print(urllib.parse.urljoin(BASE_URL, "/about"))
print(urllib.parse.urljoin(BASE_URL, "contact.html"))
print(urllib.parse.urljoin(BASE_URL, "../index.html"))

def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

def split_links(links, domain):
    internal = []
    external = []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)
    return internal, external

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fără src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a găsit exact imaginile aşteptate"
print("Testul a trecut!")

time.sleep(1)
response = requests.get(BASE_URL, timeout=TIMEOUT)

finder_real = ImageFinder()
finder_real.feed(response.text)
print(len(finder_real.images), "imagini găsite")
for src in finder_real.images:
    print(src)

def page_fingerprint(url):
    time.sleep(1)
    resp = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(resp.content).hexdigest()

print(page_fingerprint(BASE_URL))
print(page_fingerprint(BASE_URL))

with open("headers.json", "w") as file:
    json.dump(dict(response.headers), file, indent=2)

with open("headers.json", "r") as file:
    loaded_headers = json.load(file)
print("Content-Type din JSON:", loaded_headers.get("Content-Type"))

def resolve(hostname):
    return socket.gethostbyname(hostname)

print(resolve("cybercor.org"))

def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
            days_left = (expire_timestamp - time.time()) / 86400
            return int(days_left)

print(cert_days_left("cybercor.org"))