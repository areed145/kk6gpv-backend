from flask import Flask, render_template, request

from helpers import figs, flickr

app = Flask(__name__)

gals = flickr.get_gals()


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
    frames = []
    idx = 0
    for gal in gals:
        if idx < 6:
            frames.append(
                {'caption': gals[gal]['title'] + ' - ' + str(gals[gal]['count_photos']),
                 'thumb': gals[gal]['primary'],
                 'kk6gpv_link': gals[gal]['kk6gpv_link']},
            )
            idx += 1
        else:
            rows.append(frames)
            frames = []
            idx = 0
    return render_template('galleries.html', rows=rows, title='Galleries')


@app.route('/galleries/<id>')
def gallery(id):
    rows = []
    frames = []
    idx = 0
    for ph in gals[id]['photos']:
        if idx < 6:
            frames.append(
                {'thumb': gals[id]['photos'][ph]['thumb'],
                 'kk6gpv_link': '/galleries/'+id+'/'+ph},
            )
            idx += 1
        else:
            rows.append(frames)
            frames = []
            idx = 0
    return render_template('galleries.html', rows=rows, title=gals[id]['title'])


@app.route('/galleries/<id>/<ph>')
def image(id, ph):
    image = {
        'thumb': gals[id]['photos'][ph]['thumb'],
        'thumb': gals[id]['photos'][ph]['large'],
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
