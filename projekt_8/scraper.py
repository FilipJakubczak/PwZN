import threading
import requests
from timeit import default_timer as timer
from bs4 import BeautifulSoup

link = "http://www.if.pw.edu.pl/~mrow/dyd/wdprir/"
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

images = soup.select("a[href*=png]")

def download(target, location):
    img_url = target.attrs['href']
    url = link + img_url
    r = requests.get(url, stream = True)
    with open(location + img_url, 'wb') as file:
        for chunk in r.iter_content(1024):
            if chunk:
                file.write(chunk)

def download_seq(location):
    for img in images:
        download(img, location)

def download_multi(location):
    threads = []
    for img in images:
        threads.append(threading.Thread(target=download, args=(img, location)))
    for th in threads:
        th.start()
    for th in threads:
        th.join()

# sekwencyjne
start = timer()
download_seq("img/")
end = timer()
print("Pobieranie sekwencyjne: {} s".format(end - start))

# wielowątkowe
start = timer()
download_multi("img/")
end = timer()
print("Pobieranie wielowątkowe: {} s".format(end - start))