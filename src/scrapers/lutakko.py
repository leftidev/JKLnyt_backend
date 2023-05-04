import requests
#from bson import json_util
from bs4 import BeautifulSoup
import re
from scrapers.event import Event
#from event import Event
from datetime import date
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

        # hae eventin dd/mm ja nykyhetken
        dateVar = i.find('div', {'class':'date'}).span.text
        dayVar = dateVar.split(" ")[1].split(".")[0]
        monthVar = dateVar.split(dayVar)[1].replace('.', '')
        today = date.today()
        
        # tarkista menikö ekan eventin pvm jo
        if (len(events) == 0):
            if (today.month > int(monthVar)):
                continue
            if (today.month == int(monthVar)):
                if (today.day > int(dayVar)):
                    continue

        # alusta event
        event = Event("", 0, 0, 0, 0, 0, None, "", "", "", 0, 0)
        
        # ikäraja
        age = i.find('div', {'class':'age-limit'})
        # kellonaika
        time = i.find('div', {'class':'time'}).span.text
        # lippujen hinta
        tickets = i.find('div', {'role':'tickets'})

        # tarkista onko tapahtumalla hintoja
        if (tickets != None):
            idx = tickets.text.find('â‚¬')
            prices = re.sub(r"[\n\t]*", "", tickets.text[0:idx])
            priceRange = re.findall(r'\d+', prices)
            event.price = '-'.join([min(priceRange, key=int), max(priceRange, key=int)])
        else:
            event.price = "Ei tiedossa"

        # handlaa jos ikäraja-elementtiä ei ole
        if age is None:
            age = "Ei ikärajaa"
        else:
            age = age.span.text

        # aseta eventille attribuuttien arvot
        event.agelimit = age
        event.day = dayVar
        event.month = monthVar
        event.tstart = time.split('-')[0]
        event.tend = time.split('-')[1]
        event.venue = "Tanssisali lutakko"
        event.category = "Musiikki"
        event.info = 'https://jelmu.net'
        event.lat = 62.23927497596992
        event.lon = 25.754647658270674

        # esiintyjätiedot
        spans = i.a.find_all('span')
        names = []

        for span in spans:
            # esiintyjät
            names.append(span.text)
        
        event.name = ', '.join(names)
        events.append(event)
    
    lutakko = []
    for i in events:
        #lutakko.append(json.dumps(i.__dict__, ensure_ascii=False))
        lutakko.append(i.__dict__)
        
    return lutakko