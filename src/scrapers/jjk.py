import requests
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
import json


def scrape_jjk():
    events = []

    # jjk ottelut
    resp = requests.get('https://www.jjk.fi/otteluohjelma/').text

    soup = BeautifulSoup(resp, features="html.parser")

    # ottelut listattuna p-tägeihin
    ps = soup.find_all('p', {'class':'has-vivid-red-color has-text-color'})

    # käy läpi kaikki tapahtumat
    for p in ps:
        eText = p.strong.text
        eText = eText.split(" ", 1)[1]
        date = eText.split(" ", 1)[0]
        regex = r"(?=(?:\b[01]\d|2[0-3]):[0-5]\d\b)"
        nameTime = re.split(regex, eText.split(" ", 1)[1])

        event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
        event.day = date.split(".")[0]
        event.month = date.split(".")[1]
        event.name = nameTime[0]
        event.tstart = nameTime[1]
        event.price = "Ei tiedossa"
        event.info = "https://www.jjk.fi/otteluohjelma/"
        event.agelimit = "Ei ikärajaa"
        event.category = "Urheilu"
        event.venue = "Harjun Stadion"
        event.lat = 62.244983758151776
        event.lon = 25.740459560236086
        events.append(event)

    jjk = []
    for i in events:
        #jjk.append(json.dumps(i.__dict__, ensure_ascii=False))
        jjk.append(i.__dict__)

    return jjk