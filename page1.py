from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import sys

hdr = {'User-Agent': 'Mozilla/5.0'}
base = 'http://www.5starmusiq.com/all-process.asp?action=LoadMp3Album&pgNo='
for val in range(1, 63):
    site = '%s%s' % (base, val)
    print(site)
    allsongslinks = []
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = bs(page, 'lxml')
    try:
        maindiv = soup.select("[class~=img-thumbnail] > a")
        for link in maindiv:
            link.img.decompose()
            allsongslinks.append(link.attrs['href'])
        with open("links.txt", 'a') as f:
            for item in allsongslinks:
                f.write("%s\n" % item)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise
