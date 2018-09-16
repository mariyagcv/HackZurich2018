#!/usr/bin/env python
# coding=latin-1
from flask import Flask
from flask import  render_template
from flask import request
import unicodedata
# import googlemaps
from datetime import datetime
import datetime
#@title import training file
import pandas as pd
import io
import numpy as np
import tensorflow as tf
from flask_cors import CORS

df = None
df = pd.read_csv('./filename.csv', sep=';', parse_dates = True, index_col=0)
  # df = pd.read_csv(io.StringIO(uploaded[fn].decode('utf-8')), sep=';', parse_dates=True,
    # index_col=0)
df.drop('sensor_id', axis=1, inplace=True)

#@title Clean training data and add all features
df_grouped = df.groupby(pd.Grouper(freq='30Min')).sum()

# Test against predicting people inside vs flow
df_grouped['total_inside'] = df_grouped['in_count'] + df_grouped['out_count']
# df_grouped['total_flow'] = df_grouped['in_count'] + df_grouped['out_count']

index_copy = df_grouped.index.copy()

# encode day
df_grouped['day_code'] = index_copy.weekday
# encode time
df_grouped['time'] = np.array(list(map(lambda x: datetime.timedelta(hours=x.hour, minutes=x.minute, seconds=x.second).total_seconds(), index_copy.time)))
df_grouped.drop('in_count', axis=1, inplace=True)
df_grouped.drop('out_count', axis=1, inplace=True)

# TODO: Include tempreature and real life events
# Minimise total_inside using day_code and time
# Sample training and testing
msk = np.random.rand(len(df_grouped)) < 0.8
training_set = df_grouped[msk].copy()
training_set.drop('total_inside', axis=1, inplace=True)
training_set = training_set.values
training_set_y = df_grouped[msk].copy().values

testing_set = df_grouped[~msk].values

# used to parse the backend request, given a time in format 15:30 string will extract total seconds from start of the day
def parse_time_given(time_str):
  datetime_object = datetime.datetime.strptime(time_str, '%H-%M')
  time_seconds = datetime.timedelta(hours=datetime_object.hour, minutes=datetime_object.minute, seconds=datetime_object.second).total_seconds()
  return time_seconds

training_values = tf.placeholder("float",[None,2])
test_values     = tf.placeholder("float",[2])
distance = tf.reduce_sum(tf.abs(tf.add(training_values,tf.negative(test_values))),reduction_indices=1)
prediction_factor = tf.arg_min(distance,0)
init = tf.initialize_all_variables()

# if you are running this as a service, no need to do with tf.session, instead just start the session and never close it
sess = tf.Session()
sess.run(init)


# we default to sunday when we don't have a day, which is because this is a hackathon
def get_prediction(time_in_seconds, day_of_the_week = 6):
  testing_value = np.array([time_in_seconds, day_of_the_week])
  index_in_trainingset = sess.run(prediction_factor,feed_dict={training_values:training_set,test_values:testing_value})
  return training_set_y[index_in_trainingset][0]

# output of the network: [num of people, time in total seconds from start of the day, the day of the week encoded (e.g. friday is 5)]


app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/prediction', methods = ['GET'])
def received():
    t = request.args.get('arrival_time')
    print (t)
    return str(get_prediction(parse_time_given(t)))
