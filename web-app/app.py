import time
import atexit
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from helpers import figs, flickr

app = Flask(__name__)

sched = BackgroundScheduler(daemon=True)
sched.add_job(flickr.get_gals, 'interval', hours=1)
sched.start()

sid = 'KTXHOUST1941'

times = dict(m_5='5m', h_1='1h', h_6='6h', d_1='1d',
             d_2='2d', d_7='7d', d_30='30d')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@app.route('/')
def index():
    wx = figs.get_wx_latest(sid)
    return render_template('index.html', wx=wx)


@app.route('/awc')
def awc():
    prop_awc = 'flight_category'
    map_awc = figs.create_map_awc(prop_awc)
    return render_template('awc.html', plot=map_awc)


@app.route('/wx')
def wx():
    time_wx = 'd_1'
    fig_td, fig_pr, fig_pc, fig_wd, fig_su, fig_wr = figs.create_wx_figs(
        time_wx, sid)
    return render_template('wx.html', times=times, fig_td=fig_td, fig_pr=fig_pr, fig_pc=fig_pc, fig_wd=fig_wd, fig_su=fig_su, fig_wr=fig_wr)


@app.route('/iot')
def iot():
    sensor_iot = 'sensor.load_1m'
    time_iot = 'h_6'
    graph_iot = figs.create_graph_iot(sensor_iot, time_iot)
    return render_template('iot.html', times=times, plot=graph_iot)


@app.route('/aprs')
def aprs():
    type_aprs = 'radius'
    prop_aprs = 'speed'
    time_aprs = 'h_1'
    map_aprs, plot_speed, plot_alt, plot_course, rows = figs.create_map_aprs(
        type_aprs, prop_aprs, time_aprs)
    return render_template('aprs.html', times=times, map_aprs=map_aprs, plot_speed=plot_speed, plot_alt=plot_alt, plot_course=plot_course, rows=rows)


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
    rows = flickr.get_gal_rows(6)
    return render_template('galleries.html', rows=rows, title='Galleries')


@app.route('/galleries/<id>')
def gallery(id):
    rows, gals = flickr.get_photo_rows(id, 6)
    return render_template('galleries.html', rows=rows, title=gals[id]['title'])


@app.route('/galleries/<id>/<ph>')
def image(id, ph):
    gals = flickr.load_gals()
    image = {
        'thumb': gals[id]['photos'][ph]['thumb'],
        'large': gals[id]['photos'][ph]['large'],
    }
    return render_template('image.html', image=image, title='photo')


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
    map_oilgas = figs.create_map_oilgas()
    return render_template('oilgas.html', plot=map_oilgas)


@app.route('/oilgas2')
def oilgas2():
    # map_oilgas2 = figs.create_map_oilgas2()
    # map_oilgas2.save('templates/map.html')
    return render_template('oilgas2.html')

@app.route('/about')
def test():
    return render_template('about.html')


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = figs.create_plot(feature)
    return graphJSON


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
    data["map_aprs"] = json.loads(map_aprs)
    data["plot_speed"] = json.loads(plot_speed)
    data["plot_alt"] = json.loads(plot_alt)
    data["plot_course"] = json.loads(plot_course)
    data["rows"] = rows
    return json.dumps(data, default=myconverter)


@app.route('/graph_wx', methods=['GET', 'POST'])
def graph_wx_change():
    time_wx = request.args['time_wx']
    fig_td, fig_pr, fig_pc, fig_wd, fig_su, fig_wr = figs.create_wx_figs(
        time_wx, sid)
    data = {}
    data["fig_td"] = json.loads(fig_td)
    data["fig_pr"] = json.loads(fig_pr)
    data["fig_pc"] = json.loads(fig_pc)
    data["fig_wd"] = json.loads(fig_wd)
    data["fig_su"] = json.loads(fig_su)
    data["fig_wr"] = json.loads(fig_wr)
    return json.dumps(data, default=myconverter)


@app.route('/graph_iot', methods=['GET', 'POST'])
def graph_iot_change():
    sensor_iot = request.args['sensor_iot']
    time_iot = request.args['time_iot']
    graphJSON = figs.create_graph_iot(sensor_iot, time_iot)
    return graphJSON


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
