from flask import Flask, jsonify, request

from scrapers.lutakko import scrape_lutakko


app = Flask(__name__)

# Tässä skreipataan
tapahtumat = scrape_lutakko()

@app.route('/')
def hello_world():
    return '<h1>Hello from the JKLnyt team!</h2>'

@app.get("/events")
def get_events():
    return tapahtumat


if __name__ == '__main__':
    app.run(debug=True)