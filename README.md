# JKLnyt_backend

Backend for https://github.com/jantsavlog/JKLnyt_GIT

## Prerequisites:

#### Technologies
- MongoDB <br/>
- Python <br/>

#### Python libraries
- Pymongo <br/>
- Flask <br/>
- BeautifulSoup4 <br/>
- Requests

## Functionality

- Creates a MongoDB database and a collection, then populates it with scraped event data <br/>
- Endpoint displays data from the collection as JSON

## Running locally

#### Windows:

> Install MongoDB, Python and required libs
> 
> set FLASK_APP=app.py <br/>
> set FLASK_ENV=development <br/>
> py -m flask run

#### Check out in browser:

> http://127.0.0.1:5000/get