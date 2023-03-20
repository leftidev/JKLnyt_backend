# JKLnyt_backend

Backend for https://github.com/jantsavlog/JKLnyt_GIT

## Prerequisites:

MongoDB <br/>
Pymongo <br/>
Flask <br/>

## How to run locally?

#### Windows:

> set FLASK_APP=app.py <br/>
> set FLASK_ENV=development <br/>
> py -m flask run

#### Check out in browser:

> http://127.0.0.1:5000/get

#### Note:

> Creates a Mongo database and a collection -> populates it with scraped event data <br/>
> Endpoint displays data from the collection as JSON
