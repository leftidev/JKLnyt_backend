class Event:
  def __init__(self, name, day, month, tstart, tend, price, agelimit, info, venue, category, lat, lon):
    self.name = name
    self.day = day
    self.month = month
    self.tstart = tstart
    self.tend = tend
    self.price = price
    self.agelimit = agelimit
    self.info = info
    self.venue = venue
    self.category = category
    self.lat = lat
    self.lon = lon