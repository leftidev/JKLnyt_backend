import requests
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
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
            event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
            textSplit = eText.split(" ", 1)
            event.name = textSplit[1]
            date = textSplit[0]
            event.day = date.split(".")[0]
            event.month = date.split(".")[1]
            event.info = "https://escapejkl.fi/tapahtumat/"
            event.agelimit = "Ei tiedossa"
            event.price = "Ei tiedossa"
            events.append(event)
        

    escape = []
    for i in events:
        #escape.append(json.dumps(i.__dict__, ensure_ascii=False))
        escape.append(i.__dict__)

    return escape