from flask import Flask, jsonify, request

from scrapers.lutakko import scrape_lutakko


app = Flask(__name__)

tapahtumat = scrape_lutakko()

@app.get("/events")
def get_events():
    return tapahtumat


if __name__ == '__main__':
    app.run(debug=True)