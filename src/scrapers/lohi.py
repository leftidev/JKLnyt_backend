import requests
from bs4 import BeautifulSoup
import re
from event import Event
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
        if (home.lower() == 'lohi'):
            time = row[0]
            time = time.text.split(" ")[1].split(".")
            event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
            event.name = home + " vs " + row[2].text
            event.day = time[0]
            event.month = time[1]
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
        lohi.append(json.dumps(i.__dict__, ensure_ascii=False))

    return lohi