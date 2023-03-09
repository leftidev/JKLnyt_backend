import requests
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
import json


def scrape_lutakko():
    events = []

    # lutakon keikkojen sivu
    resp = requests.get('https://jelmu.net').text

    # testauksessa käytetty lokaalia html-dokumenttia
    # että liian monet http-pyynnöt ei johda ip-blokkaukseen
    # HTMLFile = open("lutakko.html", "rb")
    # html = HTMLFile.read()

    soup = BeautifulSoup(resp, features="html.parser")

    # eventit listattuna li-tägeihin
    li = soup.find_all('li')

    # käy läpi kaikki tapahtumat
    for i in li:
        if i.a.span is None:
            continue

        # alusta event
        event = Event("", 0, 0, 0, 0, 0, None)
        # päivämäärä
        date = i.find('div', {'class':'date'}).span.text
        # ikäraja
        age = i.find('div', {'class':'age-limit'})
        # kellonaika
        time = i.find('div', {'class':'time'}).span.text
        # lippujen hinta
        tickets = i.find('div', {'role':'tickets'})
        idx = tickets.text.find('â‚¬')
        prices = re.sub(r"[\n\t]*", "", tickets.text[0:idx])
        priceRange = re.findall(r'\d+', prices)

        # handlaa jos ikäraja-elementtiä ei ole
        if age is None:
            age = "Ei ikärajaa"
        else:
            age = age.span.text

        # aseta eventille attribuuttien arvot
        event.price = '-'.join([min(priceRange, key=int), max(priceRange, key=int)])
        event.agelimit = age
        event.day = date.split(" ")[1].split(".")[0]
        event.month = date.split(event.day)[1].replace('.', '')
        event.tstart = time.split('-')[0]
        event.tend = time.split('-')[1]

        # esiintyjätiedot
        spans = i.a.find_all('span')
        names = []

        for span in spans:
            # esiintyjät
            names.append(span.text)
        
        event.name = ' '.join(names)
        events.append(event)

    lutakko = []
    for i in events:
        lutakko.append(json.dumps(i.__dict__, ensure_ascii=False))

    return lutakko