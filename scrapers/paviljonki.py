import requests
import re
from bs4 import BeautifulSoup
from event import Event

events = []

# resp = requests.get('https://www.paviljonki.fi/tapahtumat-liput/').text
# print(resp)

HTMLFile = open("paviljonki.html", "rb")
html = HTMLFile.read()

soup = BeautifulSoup(html, features="html.parser")
divs = soup.find_all("div", {"class": "event-list-item"})

for d in divs:
    event = Event("", 0, 0, 0, 0, 0, 0)
    event.name = d.find("h2", {"class":"event-details__title"}).text.strip()
    details = d.find("div", {"class":"event-details__meta"}).text
    print(details)