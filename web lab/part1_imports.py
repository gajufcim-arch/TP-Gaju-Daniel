

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 
import requests
print("Versiune requests:", requests.__version__)





raspuns_ex2_stil1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status Ex 2 (stil 1):", raspuns_ex2_stil1.status_code)

from requests import get
raspuns_ex2_stil2 = get(BASE_URL, timeout=TIMEOUT)
print("Status Ex 2 (stil 2):", raspuns_ex2_stil2.status_code)




import requests as rq
raspuns_ex3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Status Ex 3:", raspuns_ex3.status_code)
ă 'rq').


raspuns_ex4 = urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
print("Status Ex 4:", raspuns_ex4.status)


corp_text = raspuns_ex4.read().decode("utf-8")
print("Primele 200 caractere Ex 4:\n", corp_text[:200])







raspuns_ex6 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 6 s-a executat cu succes folosind timeout.")



timp_start = time.perf_counter()
raspuns_ex7 = requests.get(BASE_URL, timeout=TIMEOUT)
timp_stop = time.perf_counter()

timp_total_masurat = timp_stop - timp_start
timp_elapsed = raspuns_ex7.elapsed.total_seconds()

print(f"Timp măsurat cu perf_counter: {timp_total_masurat:.4f} sec")
print(f"Timp raportat de response.elapsed: {timp_elapsed:.4f} sec")





try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")