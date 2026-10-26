import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

response = requests.get(BASE_URL, timeout=TIMEOUT)

print(response.status_code)
print(response.ok)
print(response.url)
print(response.encoding)

response.raise_for_status()

time.sleep(1)
try:
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError:
    print("Eroare: Pagina căutată nu a fost găsită pe server.")

for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

print(response.headers.get("Server", "lipsește"))
print(response.headers.get("Content-Type", "lipsește"))
print(response.headers.get("content-type", "lipsește"))

print(response.text.lower().count("cyber"))

html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
print(html[start:end].strip())

lines = html.splitlines()
print(len(lines))
print(len(max(lines, key=len)))

if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

time.sleep(1)
response_redir = requests.get("http://cybercor.org", timeout=TIMEOUT)
for redirect in response_redir.history:
    print(redirect.status_code, redirect.url)
print(response_redir.url)

time.sleep(1)
req_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
req_get = requests.get(BASE_URL, timeout=TIMEOUT)
print(len(req_head.content))
print(len(req_get.content))

if response.cookies:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)
else:
    print("Niciun cookie setat")

session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Student"})
time.sleep(1)
response_session = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(response_session.json())