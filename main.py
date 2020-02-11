#!/usr/bin/env python3

import socketserver
import http.server
import requests
import sys

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
INDEX_HTTP_FILE = "index.html"
AVG_ITERATION = 10
HTTP_PORT = 8080

"""
httpRequestHandler Class to serve a file via /
"""
class httpRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Override do_Get of class SimpleHTTPRequestHandler to set to a desired .html file
    def do_GET(self):
        if self.path == '/':
            self.path = INDEX_HTTP_FILE
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

"""
Handles HTTP server, serves forever
"""
def handleHTTP():
    try:
        handler = httpRequestHandler
    except OSError as e:
        print(e)
        sys.exit(1)

    server = socketserver.TCPServer(("", HTTP_PORT), handler)
    server.serve_forever()

"""
Prints string to a simple html file
"""
def printToFile(s):
    try:
        with open(INDEX_HTTP_FILE, "a") as file:
            file.write(s + '<br>')
    except IOError as e:
        print(e)
        sys.exit(1)

"""
Calculate average of a list
"""
def average(l):
    return sum(l) / len(l)

"""
Get bitcoin price from coinmargetcap API
"""
def getLatestBitcoinPrice():
    try:
        response = requests.get(TICKER_API_URL+'bitcoin')
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    responseJson = response.json()
    return float(responseJson[0]['price_usd'])

"""
Print bitcoin price every minute, calculate average every AVG_ITERATION
"""
def run(sc, priceArr, counter):
    price = getLatestBitcoinPrice()
    if not price:
        print("getLatestBitcoinPrice Failed.")
        sys.exit(1)

    printToFile(f'price = {price}')
    priceArr.append(price)
    counter += 1
    if counter == AVG_ITERATION:
        printToFile(f'average = {average(priceArr)}')
        counter = 0
        priceArr.clear()

    sc.enter(60, 1, run, (sc, priceArr, counter))

def main():
    import sched
    import time
    import threading

    # Run as different thread
    x = threading.Thread(target=handleHTTP)
    x.start()

    s = sched.scheduler(time.time, time.sleep)
    s.enter(0, 1, run, (s, [], 0))
    s.run()

if __name__ == '__main__':
    main()