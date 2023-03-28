import requests
import re
from bs4 import BeautifulSoup
from event import Event
import json

def scrape_paviljonki():

    events = []

    resp = requests.get('https://www.paviljonki.fi/tapahtumat-liput/').text
    #print(resp)

    # HTMLFile = open("paviljonki.html", "rb")
    # html = HTMLFile.read()

    soup = BeautifulSoup(resp, features="html.parser")
    divs = soup.find_all("div", {"class": "event-list-item"})

    for d in divs:
        ahref = d.find("h2", {"class":"event-details__title"}).a
        event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)

        event.name = ahref.text.strip()
        time = d.find("div", {"class": "event-details__meta"}).text.strip()
        times = time.splitlines()
        date = times[-1].replace('\t', '')
        event.day = date.split('.')[0]
        event.month = date.split('.')[1]
        event.info = ahref.get("href")
        event.venue = "Paviljonki"
        event.lat = 62.24031954660093
        event.lon = 25.757825059521508
        cat = d.find("span", {"class":"tag-list-item"}).text
        event.category = cat
        events.append(event)

    paviljonki = []
    for i in events:
        paviljonki.append(json.dumps(i.__dict__, ensure_ascii=False))

    return paviljonki