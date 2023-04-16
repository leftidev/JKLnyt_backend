from flask import Flask, jsonify, request
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

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

# Create a MongoDB collection for events
collection = db['events']

# Define API key for testing
API_KEY = '123456'
    
# Define a function to scrape data from venues and insert it into the MongoDB collection
def scrape_and_insert():
    collection.drop()
    tapahtumat_lutakko = scrape_lutakko();
    tapahtumat_paviljonki = scrape_paviljonki();
    tapahtumat_lohi = scrape_lohi();
    tapahtumat_jjk = scrape_jjk();
    tapahtumat_escape = scrape_escape();

    collection.insert_many(tapahtumat_lutakko)
    collection.insert_many(tapahtumat_paviljonki)
    collection.insert_many(tapahtumat_lohi)
    collection.insert_many(tapahtumat_jjk)
    collection.insert_many(tapahtumat_escape)
    # Debug print
    print('Data inserted to collection "events" succesfully')

# Create a scheduler to run the scraper function every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_and_insert, trigger='interval', seconds=10)
scheduler.start()

# Retrieves all the data from MongoDB collection, converts the _id field to a string (because it's not JSON serializable by default), and returns the data as a JSON response
@app.route('/get', methods=['GET'])
def get_data():
    # Note that this is a simple way to add API key authentication, but it's not the most secure method. 
    # A more secure approach would involve using a token-based authentication system, such as OAuth2.
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized access'}), 401
    
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append(item)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)