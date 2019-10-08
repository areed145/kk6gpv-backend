import os
import time
import atexit
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, g
from helpers import figs, flickr

from flask_mongoengine import MongoEngine
import mongoengine as me
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoEngineStorage
from flask_track_usage.storage.output import OutputWriter
from flask_track_usage.storage.printer import PrintWriter
from flask_track_usage.summarization import sumUrl, sumRemote, sumUserAgent, sumLanguage, sumServer

app = Flask(__name__)

sid = os.environ['SID']

times = dict(m_5='5m', h_1='1h', h_6='6h', d_1='1d',
             d_2='2d', d_7='7d', d_30='30d')

app.config['MONGODB_SETTINGS'] = {
    'db': 'coconut_barometer_stats',
    'host': os.environ['MONGODB_CLIENT']
    }
app.config['TRACK_USAGE_USE_FREEGEOIP'] = True
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'
app.config['TRACK_USAGE_COOKIE'] = True

mongo_db =MongoEngine(app)

t = TrackUsage(app, [
    PrintWriter(),
    OutputWriter(transform=lambda s: 'OUTPUT: ' + str(s)),
    MongoEngineStorage(hooks=[sumUrl, sumRemote, sumUserAgent, sumLanguage, sumServer]),
])

sched = BackgroundScheduler(daemon=True)
sched.add_job(flickr.get_gals, 'interval', hours=1)
sched.start()


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@t.include
@app.route('/')
def index():
    g.track_var['page'] = 'home'
    wx = figs.get_wx_latest(sid)
    return render_template('index.html', wx=wx)


@t.include
@app.route('/awc')
def awc():
    g.track_var['page'] = 'awc'
    prop_awc = 'flight_category'
    map_awc = figs.create_map_awc(prop_awc)
    return render_template('awc.html', plot=map_awc)


@t.include
@app.route('/wx')
def wx():
    g.track_var['page'] = 'wx'
    time_wx = 'd_1'
    fig_td, fig_pr, fig_pc, fig_wd, fig_su, fig_wr = figs.create_wx_figs(
        time_wx, sid)
    return render_template('wx.html', times=times, fig_td=fig_td, fig_pr=fig_pr, fig_pc=fig_pc, fig_wd=fig_wd, fig_su=fig_su, fig_wr=fig_wr)


@t.include
@app.route('/iot')
def iot():
    g.track_var['page'] = 'iot'
    sensor_iot = 'sensor.load_1m'
    time_iot = 'm_5'
    graph_iot = figs.create_graph_iot(sensor_iot, time_iot)
    return render_template('iot.html', times=times, plot=graph_iot)


@t.include
@app.route('/aprs')
def aprs():
    g.track_var['page'] = 'aprs'
    type_aprs = 'radius'
    prop_aprs = 'speed'
    time_aprs = 'm_5'
    map_aprs, plot_speed, plot_alt, plot_course, rows = figs.create_map_aprs(
        type_aprs, prop_aprs, time_aprs)
    return render_template('aprs.html', times=times, map_aprs=map_aprs, plot_speed=plot_speed, plot_alt=plot_alt, plot_course=plot_course, rows=rows)


@t.include
@app.route('/aircraft')
def aircraft():
    g.track_var['page'] = 'aircraft'
    return render_template('aircraft.html')


@t.include
@app.route('/paragliding')
def paragliding():
    g.track_var['page'] = 'paragliding'
    return render_template('paragliding.html')


@t.include
@app.route('/soaring')
def soaring():
    g.track_var['page'] = 'soaring'
    return render_template('soaring.html')


@t.include
@app.route('/n5777v')
def n5777v():
    g.track_var['page'] = 'n5777v'
    return render_template('n5777v.html')


@t.include
@app.route('/galleries')
def galleries():
    g.track_var['page'] = 'galleries'
    rows = flickr.get_gal_rows(6)
    return render_template('galleries.html', rows=rows, title='Galleries')


@t.include
@app.route('/galleries/<id>')
def gallery(id):
    g.track_var['page'] = 'gallery'
    g.track_var['gallery'] = str(id)
    rows, gals = flickr.get_photo_rows(id, 6)
    return render_template('galleries.html', rows=rows, title=gals[id]['title'])


@t.include
@app.route('/galleries/<id>/<ph>')
def image(id, ph):
    g.track_var['page'] = 'photo'
    g.track_var['gallery'] = str(id)
    g.track_var['photo'] = str(ph)
    gals = flickr.load_gals()
    image = {
        'thumb': gals[id]['photos'][ph]['thumb'],
        'large': gals[id]['photos'][ph]['large'],
    }
    return render_template('image.html', image=image, title='photo')


@t.include
@app.route('/travel')
def travel():
    g.track_var['page'] = 'travel'
    return render_template('travel.html')


@t.include
@app.route('/scuba')
def scuba():
    g.track_var['page'] = 'scuba'
    return render_template('scuba.html')


@t.include
@app.route('/fishing')
def fishing():
    g.track_var['page'] = 'fishing'
    return render_template('fishing.html')


@t.include
@app.route('/oilgas')
def oilgas():
    g.track_var['page'] = 'oilgas'
    map_oilgas = figs.create_map_oilgas()
    return render_template('oilgas.html', plot=map_oilgas)


@t.include
@app.route('/oilgas_folium')
def oilgas_folium():
    g.track_var['page'] = 'oilgas_folium'
    return render_template('oilgas_folium.html')


@t.include
@app.route('/about')
def about():
    g.track_var['page'] = 'about'
    return render_template('about.html')


@app.route('/map_awc', methods=['GET', 'POST'])
def map_awc_change():
    prop_awc = request.args['prop_awc']
    graphJSON = figs.create_map_awc(prop_awc)
    return graphJSON


@app.route('/map_aprs', methods=['GET', 'POST'])
def map_aprs_change():
    type_aprs = request.args['type_aprs']
    prop_aprs = request.args['prop_aprs']
    time_aprs = request.args['time_aprs']
    map_aprs, plot_speed, plot_alt, plot_course, rows = figs.create_map_aprs(
        type_aprs, prop_aprs, time_aprs)
    data = {}
    data['map_aprs'] = json.loads(map_aprs)
    data['plot_speed'] = json.loads(plot_speed)
    data['plot_alt'] = json.loads(plot_alt)
    data['plot_course'] = json.loads(plot_course)
    data['rows'] = rows
    return json.dumps(data, default=myconverter)


@app.route('/graph_wx', methods=['GET', 'POST'])
def graph_wx_change():
    time_wx = request.args['time_wx']
    fig_td, fig_pr, fig_pc, fig_wd, fig_su, fig_wr = figs.create_wx_figs(
        time_wx, sid)
    data = {}
    data['fig_td'] = json.loads(fig_td)
    data['fig_pr'] = json.loads(fig_pr)
    data['fig_pc'] = json.loads(fig_pc)
    data['fig_wd'] = json.loads(fig_wd)
    data['fig_su'] = json.loads(fig_su)
    data['fig_wr'] = json.loads(fig_wr)
    return json.dumps(data, default=myconverter)


@app.route('/graph_iot', methods=['GET', 'POST'])
def graph_iot_change():
    sensor_iot = request.args['sensor_iot']
    time_iot = request.args['time_iot']
    graphJSON = figs.create_graph_iot(sensor_iot, time_iot)
    return graphJSON


@app.route('/create_oilgas_folium')
def create_oilgas_folium():
    figs.create_map_oilgas_folium().save('templates/map.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
