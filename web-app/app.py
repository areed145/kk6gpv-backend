import os
import time
import atexit
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, session, g, redirect, render_template_string, make_response
from helpers import figs, flickr
from helpers.blog import Database, Blog, Post, User

from pymongo import MongoClient
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoPiggybackStorage
from flask_caching import Cache

import json
import feather
import pandas as pd

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

sid = os.environ['SID']

client = MongoClient(os.environ['MONGODB_CLIENT'])
db = client.coconut_barometer
stats = db.stats

app.secret_key = "secret"

times = dict(m_5='5m', h_1='1h', h_6='6h', d_1='1d',
             d_2='2d', d_7='7d', d_30='30d')

app.config['TRACK_USAGE_USE_FREEGEOIP'] = True
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'
app.config['TRACK_USAGE_COOKIE'] = True

t = TrackUsage(app, [MongoPiggybackStorage(stats)])

sched = BackgroundScheduler(daemon=True)
sched.add_job(flickr.get_gals, 'interval', hours=1)
sched.start()


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@cache.cached(timeout=60)
@t.include
@app.route('/')
def index():
    g.track_var['page'] = 'home'
    wx = figs.get_wx_latest(sid)
    return render_template('index.html', wx=wx)


@cache.cached(timeout=60)
@t.include
@app.route('/awc')
def awc():
    g.track_var['page'] = 'awc'
    prop_awc = 'flight_category'
    map_awc = figs.create_map_awc(prop_awc)
    return render_template('awc.html', plot=map_awc)


@cache.cached(timeout=60)
@t.include
@app.route('/wx')
def wx():
    g.track_var['page'] = 'wx'
    time_wx = 'd_1'
    fig_td, fig_pr, fig_cb, fig_pc, fig_wd, fig_su, fig_wr, fig_thp = figs.create_wx_figs(
        time_wx, sid)
    return render_template('wx.html', times=times, fig_td=fig_td, fig_pr=fig_pr, fig_cb=fig_cb, fig_pc=fig_pc, fig_wd=fig_wd, fig_su=fig_su, fig_wr=fig_wr, fig_thp=fig_thp)


@cache.cached(timeout=60)
@t.include
@app.route('/blips')
def blips():
    g.track_var['page'] = 'blips'
    return render_template('blips.html')


@cache.cached(timeout=60)
@t.include
@app.route('/soundings')
def soundings():
    g.track_var['page'] = 'soundings'
    return render_template('soundings.html')


@cache.cached(timeout=60)
@t.include
@app.route('/iot')
def iot():
    g.track_var['page'] = 'iot'
    sensor_iot = ['sensor.load_1m']
    time_iot = 'm_5'
    graph_iot = figs.create_graph_iot(sensor_iot, time_iot)
    return render_template('iot.html', times=times, plot=graph_iot)


@cache.cached(timeout=6)
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


@cache.cached(timeout=60)
@t.include
@app.route('/aircraft')
def aircraft():
    g.track_var['page'] = 'aircraft'
    return render_template('aircraft.html')


@cache.cached(timeout=60)
@t.include
@app.route('/paragliding')
def paragliding():
    g.track_var['page'] = 'paragliding'
    return render_template('paragliding.html')


@cache.cached(timeout=60)
@t.include
@app.route('/soaring')
def soaring():
    g.track_var['page'] = 'soaring'
    return render_template('soaring.html')


@cache.cached(timeout=60)
@t.include
@app.route('/n5777v')
def n5777v():
    g.track_var['page'] = 'n5777v'
    return render_template('n5777v.html')


@cache.cached(timeout=60)
@t.include
@app.route('/galleries')
def galleries():
    g.track_var['page'] = 'galleries'
    rows = flickr.get_gal_rows(6)
    return render_template('galleries.html', rows=rows, title='Galleries')


@cache.cached(timeout=60)
@t.include
@app.route('/galleries/<id>')
def gallery(id):
    g.track_var['page'] = 'gallery'
    g.track_var['gallery'] = str(id)
    rows, gals = flickr.get_photo_rows(id, 6)
    return render_template('galleries.html', rows=rows, title=gals[id]['title'])


@cache.cached(timeout=60)
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


@cache.cached(timeout=60)
@t.include
@app.route('/travel')
def travel():
    g.track_var['page'] = 'travel'
    return render_template('travel.html')


@cache.cached(timeout=60)
@t.include
@app.route('/scuba')
def scuba():
    g.track_var['page'] = 'scuba'
    return render_template('scuba.html')


@cache.cached(timeout=60)
@t.include
@app.route('/fishing')
def fishing():
    g.track_var['page'] = 'fishing'
    return render_template('fishing.html')


@cache.cached(timeout=60)
@t.include
@app.route('/oilgas/map')
def oilgas_map():
    g.track_var['page'] = 'oilgas/map'
    with open('static/oilgas.json') as json_file:
        map_oilgas = json.load(json_file)
    return render_template('oilgas_map.html', plot=map_oilgas)


@cache.cached(timeout=60)
@t.include
@app.route('/oilgas/summary')
def oilgas_summary():
    g.track_var['page'] = 'oilgas/summary'
    df = pd.read_feather('static/oilgas_sum.feather')
    df = df.dropna(axis=0)
    df.sort_values(by='oil_cum', inplace=True, ascending=False)
    df = df[:10000]
    rows = []
    for _, row in df.iterrows():
        r = {}
        r['field'] = row['field']
        r['lease'] = row['lease']
        r['well'] = row['well']
        r['operator'] = row['operator']
        r['api'] = row['api']
        r['oil_cum'] = row['oil_cum']
        r['water_cum'] = row['water_cum']
        r['gas_cum'] = row['gas_cum']
        r['wtrstm_cum'] = row['wtrstm_cum']
        rows.append(r)
    return render_template('oilgas_summary.html', rows=rows)


@cache.cached(timeout=60)
@t.include
@app.route('/oilgas/details/<api>')
def oilgas_detail(api):
    g.track_var['page'] = 'oilgas/details'
    g.track_var['api'] = str(api)
    graph_oilgas, map_oilgas, header = figs.get_graph_oilgas(str(api))
    return render_template('oilgas_details.html', plot=graph_oilgas, map=map_oilgas, header=header)


@cache.cached(timeout=60)
@t.include
@app.route('/oilgas/mapbox')
def oilgas_mapbox():
    g.track_var['page'] = 'oilgas/mapbox'
    return render_template('oilgas_mapbox.html')


@cache.cached(timeout=60)
@t.include
@app.route('/about')
def about():
    g.track_var['page'] = 'about'
    return render_template('about.html')


# @app.route('/blogfront')
# def home_template():
#     return render_template('home.html')


@app.route('/login')  # www.my_site.com/api/login
def login_template():
    return render_template('login.html')
    # return "hello, world"


@app.route('/register')  # 127.0.0.1:4995/register
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        user = User.get_by_email(session['email'])
        blogs = user.get_blogs()

        return render_template('profile.html', blogs=blogs, email=user.email)
    else:
        return False


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
@app.route('/posts')
def blog_posts(blog_id='bca7359faed442669aa888a2657b331f'):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


@app.route('/awc/update', methods=['GET', 'POST'])
def map_awc_update():
    prop_awc = request.args['prop_awc']
    lat = request.args['lat']
    lon = request.args['lon']
    zoom = request.args['zoom']
    satellite = request.args['satellite']
    radar = request.args['radar']
    lightning = request.args['lightning']
    precip = request.args['precip']
    watchwarn = request.args['watchwarn']
    temp = request.args['temp']
    graphJSON = figs.create_map_awc(
        prop_awc, lat, lon, zoom, satellite, radar, lightning, precip, watchwarn, temp)
    return graphJSON


@app.route('/aprs/map', methods=['GET', 'POST'])
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


@app.route('/wx/graph', methods=['GET', 'POST'])
def graph_wx_change():
    time_wx = request.args['time_wx']
    fig_td, fig_pr, fig_cb, fig_pc, fig_wd, fig_su, fig_wr, fig_thp = figs.create_wx_figs(
        time_wx, sid)
    data = {}
    data['fig_td'] = json.loads(fig_td)
    data['fig_pr'] = json.loads(fig_pr)
    data['fig_cb'] = json.loads(fig_cb)
    data['fig_pc'] = json.loads(fig_pc)
    data['fig_wd'] = json.loads(fig_wd)
    data['fig_su'] = json.loads(fig_su)
    data['fig_wr'] = json.loads(fig_wr)
    data['fig_thp'] = json.loads(fig_thp)
    return json.dumps(data, default=myconverter)


@app.route('/iot/graph', methods=['GET', 'POST'])
def graph_iot_change():
    sensor_iot = request.args.getlist("sensor_iot[]")
    time_iot = request.args['time_iot']
    graphJSON = figs.create_graph_iot(sensor_iot, time_iot)
    return graphJSON


@app.route('/oilgas/map/create')
def create_oilgas():
    map_oilgas, sum_oilgas = figs.create_map_oilgas()
    with open('static/oilgas.json', 'w') as outfile:
        json.dump(map_oilgas, outfile)
    sum_oilgas.to_feather('static/oilgas_sum.feather')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
