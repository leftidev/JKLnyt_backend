from flask import Flask, jsonify
from pymongo import MongoClient

from scrapers.lutakko import scrape_lutakko


# Create flask app and connect to MongoDB database using PyMongo
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['lutakko']

# Scrape data from lutakko
tapahtumat = scrape_lutakko();

# Create a MongoDB collection for lutakko
collection = db['lutakko']

# Add lutakko events to database
# NOTE: This needs to be done only once when populating the database collection with content!!!!!
#collection.insert_many(tapahtumat)

@app.route('/')
def hello_world():
    return '<h1>Hello from the JKLnyt team!</h2>'

@app.get("/events")
def get_events():
    return tapahtumat

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





#On Windows, the location is <install directory>/bin/mongod.cfg. Open mongod.cfg file and check for dbPath option.

#C:\Program Files\MongoDB\Server\6.0\data

# curl http://localhost:5000/get