from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pymongo import MongoClient
from bson.objectid import ObjectId 
import json
import sys

songinfo=[]
client=MongoClient()
db=client.tamilMusicDB

hdr = {'User-Agent': 'Mozilla/5.0'}
base = 'http://www.5starmusiq.com/'
f=open('links.txt','r')
for line in f:
    songdetails={}
    site = '%s%s' % (base, line)
    print(site)
    allsongslinks = []
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = bs(page, 'lxml')
    try:
#song image
        maindiv = soup.select("[class~=img-thumbnail] > img[class~=img-responsive]")
        songdetails['imgsrc'] = maindiv[0].attrs['src']
#song movie
        maindiv = soup.select("[class~=col-md-6] > ul")
        a = maindiv[0].select("[class~=list-group-item]")
        last = a[-1]
        for t in a[:-1]:
            t_text=t.get_text()
            sep=t_text.find(':')
            k =t_text[:sep] 
            v =t_text[sep+1:]
            songdetails[k] = v
#LANG GENRE
        k1, v1 = last.get_text().split('|')
        k, v = k1.split(':')
        songdetails[k] = v
        k, v = v1.split(':')
        songdetails[k] = v

        maindiv=soup.select("div.panel-body.bg-danger > table ")
        for tr in maindiv[0].select("tr"):
            for td in tr.select("td"):
                song=td.select("strong")
                if song:
                    songdetails["song_name"]=song[0].get_text()
                song_url=td.select("a.label.label-primary")
                if song_url:
                    songdetails["song_url"]=song_url[0].attrs['href']           
            
            songdetails['_id'] = ObjectId()         
            if songdetails["song_name"]:
                print(songdetails)
                r=db.musicDetails.insert_one(songdetails)
                print(songdetails,r.inserted_id)
            songdetails["song_name"]=""
    except IndexError:
        print(line,"error")
        with open("log.txt",'a+') as logger:
            logger.write(line)
            logger.write("\n")
        continue
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    