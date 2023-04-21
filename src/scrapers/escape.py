import requests
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
# from event import Event
from datetime import date
import json


def scrape_escape():
    events = []

    # escapen tapahtumasivu
    resp = requests.get('https://escapejkl.fi/tapahtumat/').text

    soup = BeautifulSoup(resp, features="html.parser")

    # eventit listattuna p-tägeihin
    ps = soup.find_all('div', {'class':'et_pb_text_inner'})[2]

    # käy läpi kaikki tapahtumat
    for p in ps:
        eText = p.text
        # suodata tyhjät pois
        if (eText.strip() != ""):
            # hae tapahtuman ja nykyhetken pvm
            textSplit = eText.split(" ", 1)
            dateVar = textSplit[0]
            dayVar = dateVar.split(".")[0]
            monthVar = dateVar.split(".")[1]
            today = date.today()

            # jos ekan eventin pvm on jo mennyt, oletetaan että vanha
            if (len(events) == 0):
                # jos kuukaus on mennyt, kokeile seuraavaa
                if (today.month > int(monthVar)):
                    continue
                if (today.month == int(monthVar)):
                    # jos pv on vanha, seuraava
                    if (today.day > int(dayVar)):
                        continue

            # jos ei vanha event, luo Event objekti
            event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
            event.name = textSplit[1]
            event.day = dayVar
            event.month = monthVar
            event.info = "https://escapejkl.fi/tapahtumat/"
            event.agelimit = "Ei tiedossa"
            event.price = "Ei tiedossa"
            event.category = "Musiikki"
            event.venue = "Club Escape"
            event.lat = 62.24392610962945
            event.lon = 25.74999909853728
            events.append(event)
        

    escape = []
    for i in events:
        #escape.append(json.dumps(i.__dict__, ensure_ascii=False))
        escape.append(i.__dict__)

    return escape