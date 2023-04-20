import requests
import re
from bs4 import BeautifulSoup
from scrapers.event import Event
#from event import Event
from datetime import date
import json

def scrape_paviljonki():

    events = []

    resp = requests.get('https://www.paviljonki.fi/tapahtumat-liput/').text

    soup = BeautifulSoup(resp, features="html.parser")
    divs = soup.find_all("div", {"class": "event-list-item"})

    for d in divs:
        ahref = d.find("h2", {"class":"event-details__title"}).a

        # hae tapahtuman ja nykyhetken pvm
        time = d.find("div", {"class": "event-details__meta"}).text.strip()
        times = time.splitlines()
        dateVar = times[-1].replace('\t', '')
        dayVar = dateVar.split('.')[0]
        monthVar = dateVar.split('.')[1]
        today = date.today()

        # jos eka event on jo mennyt, mene seuraavaan
        if (len(events) == 0):
            if (today.month > int(monthVar)):
                continue
            if (today.month == int(monthVar)):
                if (today.day > int(dayVar)):
                    continue

        event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
        event.name = ahref.text.strip()
        event.day = dayVar
        event.month = monthVar
        event.info = ahref.get("href")
        event.venue = "Paviljonki"
        event.lat = 62.24031954660093
        event.lon = 25.757825059521508
        cat = d.find("span", {"class":"tag-list-item"}).text
        event.category = cat
        events.append(event)

    paviljonki = []
    for i in events:
        #paviljonki.append(json.dumps(i.__dict__, ensure_ascii=False))
        paviljonki.append(i.__dict__)

    return paviljonki