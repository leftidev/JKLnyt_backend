import requests
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
# from event import Event
from datetime import date
import json


def scrape_lohi():
    events = []

    # lohen ottelut
    resp = requests.get('https://jyvaskylanlohi.fi/ottelut/').text

    soup = BeautifulSoup(resp, features="html.parser")

    # ottelut listattuna taulukossa
    tbody = soup.find_all('figure', {'class':'wp-block-table is-style-regular'})[0].table.tbody
    trs = tbody.find_all('tr')

    # käy läpi kaikki ottelut
    for tr in trs:
        row = tr.find_all('td')
        home = row[1].text

        # etsi vain kotiottelut
        if (home.lower() == 'lohi'):
            # hae eventin ja nykyhetken dd/mm
            time = row[0]
            time = time.text.split(" ")[1].split(".")
            dayVar = time[0]
            monthVar = time[1]
            today = date.today()

            # jos eka event on jo mennyt, mene seuraavaan
            if (len(events) == 0):
                if (today.month > int(monthVar)):
                    continue
                if (today.month == int(monthVar)):
                    if (today.day > int(dayVar)):
                        continue

            event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
            event.name = home + " vs " + row[2].text
            event.day = dayVar
            event.month = monthVar
            event.agelimit = "Ei ikärajaa"
            event.price = "Ei tiedossa"
            event.info = "https://jyvaskylanlohi.fi/ottelut/"
            event.category = "Urheilu"
            event.venue = "Koskenharjun kenttä"
            event.lat = 62.257963560783836
            event.lon = 25.750349812082813

            if (len(time) > 3):
                event.tstart = time[2]+":"+time[3]
            else:
                event.tstart = time[2]

            events.append(event)

    lohi = []
    for i in events:
        #lohi.append(json.dumps(i.__dict__, ensure_ascii=False))
        lohi.append(i.__dict__)

    return lohi