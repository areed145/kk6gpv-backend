from flask import Flask, render_template, request

import flickr_api as f
from figures import figs

import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
import json

from pymongo import MongoClient

app = Flask(__name__)

f.set_keys(api_key='77a2ae7ea816558f00e4dd32249be54e', api_secret='2267640a7461db21')
f.set_auth_handler('helpers/auth')
username = '- Adam Reeder -'
u = f.Person.findByUserName(username)
ps = u.getPhotosets()

@app.route('/')
def index():
    feature = 'bar'
    bar = figs.create_plot(feature)
    return render_template('index.html', plot=bar)


@app.route('/awc')
def awc():
    return render_template('awc.html')


@app.route('/wx')
def wx():
    return render_template('wx.html')


@app.route('/iot')
def iot():
    sensor_iot = 'sensor.load_1m'
    time_iot = 't_100'
    graph_iot = figs.create_graph_iot(sensor_iot, time_iot)
    return render_template('iot.html', plot=graph_iot)


@app.route('/aprs')
def aprs():
    type_aprs = 'prefix'
    prop_aprs = 'altitude'
    time_aprs = 't_100'
    map_aprs = figs.create_map_aprs(type_aprs, prop_aprs, time_aprs)
    return render_template('aprs.html', plot=map_aprs)


@app.route('/aircraft')
def aircraft():
    return render_template('aircraft.html')


@app.route('/paragliding')
def paragliding():
    return render_template('paragliding.html')


@app.route('/soaring')
def soaring():
    return render_template('soaring.html')


@app.route('/n5777v')
def n5777v():
    return render_template('n5777v.html')


@app.route('/galleries')
def galleries():
    rows = []
    gals = []
    idx = 0
    for p in ps:
        if idx < 4:
            title = p.title
            pid = p.id
            photos = p.count_photos
            views = p.count_views
            primary = 'https://live.staticflickr.com/8203/'+p.primary+'_'+p.secret+'_q_d.jpg'
            link = 'https://www.flickr.com/photos/adamreeder/albums/'+p.id
            gals.append({'title':title, 'id':pid, 'photos':photos, 'views':views, 'primary':primary, 'link':link})
            idx += 1
        else:
            rows.append(gals)
            gals = []
            idx = 0

    return render_template('galleries.html', rows=rows)


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/scuba')
def scuba():
    return render_template('scuba.html')


@app.route('/fishing')
def fishing():
    return render_template('fishing.html')


@app.route('/oilgas')
def oilgas():
    return render_template('oilgas.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = figs.create_plot(feature)
    return graphJSON


@app.route('/map_aprs', methods=['GET', 'POST'])
def map_aprs_change():
    type_aprs = request.args['type_aprs']
    prop_aprs = request.args['prop_aprs']
    time_aprs = request.args['time_aprs']
    graphJSON = figs.create_map_aprs(type_aprs, prop_aprs, time_aprs)
    return graphJSON


@app.route('/graph_iot', methods=['GET', 'POST'])
def graph_iot_change():
    sensor_iot = request.args['sensor_iot']
    time_iot = request.args['time_iot']
    graphJSON = figs.create_graph_iot(sensor_iot, time_iot)
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
