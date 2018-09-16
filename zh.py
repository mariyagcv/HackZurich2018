#!/usr/bin/env python
# coding=latin-1
from flask import Flask
from flask import  render_template
from flask import request
import unicodedata
import googlemaps
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
