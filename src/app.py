from flask import Flask, jsonify
from pymongo import MongoClient

from scrapers.lutakko import scrape_lutakko
from scrapers.paviljonki import scrape_paviljonki
from scrapers.lohi import scrape_lohi
from scrapers.jjk import scrape_jjk
from scrapers.escape import scrape_escape


# Create flask app and connect to MongoDB database using PyMongo
app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")

# Testing on localhost
#client = MongoClient('mongodb://localhost:27017/')

db = client['JKLnyt']

# Scrape data from venues
tapahtumat_lutakko = scrape_lutakko();
tapahtumat_paviljonki = scrape_paviljonki();
tapahtumat_lohi = scrape_lohi();
tapahtumat_jjk = scrape_jjk();
tapahtumat_escape = scrape_escape();

# Create a MongoDB collection for events
collection = db['events']

# Add scraped events to database
# NOTE: This needs to be done only when populating the database collection with content!!!!!
collection.insert_many(tapahtumat_lutakko)
collection.insert_many(tapahtumat_paviljonki)
collection.insert_many(tapahtumat_lohi)
collection.insert_many(tapahtumat_jjk)
collection.insert_many(tapahtumat_escape)

@app.route('/')
def hello_world():
    return '<h1>Hello from the JKLnyt team!</h2>'

@app.get("/events")
def get_events():
    return tapahtumat_lutakko

# Retrieves all the data from MongoDB collection, converts the _id field to a string (because it's not JSON serializable by default), and returns the data as a JSON response
@app.route('/get', methods=['GET'])
def get_data():
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append(item)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)