#!/usr/bin/env python
# coding=latin-1
from flask import Flask
from flask import  render_template
from flask import request
import unicodedata
# import googlemaps
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/prediction', methods = ['GET'])
def received():
    time = request.args.get('arrival_time')
    print (time)
    return "5"
#
# def formInput():
#     start = request.form['start']
#     end = request.form['end']
#     # end = request.form['end'].encode('utf-8')
#
#
# # requesting ricetions and stuffz
#
#     gmaps = googlemaps.Client(key='AIzaSyCOcZOEW2Q07uQmpCDj4VCBanEW1yJerBM')
#
#     # # Geocoding an address
#     # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#     #
#     # # Look up an address with reverse geocoding
#     # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
#
#     # Request directions via public transit
#     now = datetime.now()
#     directions_result = gmaps.directions(start,
#                                          end,
#                                          mode="transit",
#                                          departure_time=now)
