import dns
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import time
from multiprocessing import Pool

keys_main = ('station_id', 'raw_text', 'observation_time',
             'temp_c', 'dewpoint_c', 'latitude', 'longitude',
             'wind_dir_degrees', 'wind_degrees', 'wind_speed_kt', 'wind_gust_kt',
             'altim_in_hg', 'visibility_statute_mi', 'flight_category',
             'metar_type', 'elevation_m', 'precip_in', 'wx_string')
keys_qc = ('auto', 'auto_station', 'maintenance_indicator_on', 'no_signal')
keys_sc = ('sky_cover', 'cloud_base_ft_agl')


def convert(val):
    try:
        val = float(val)
    except:
        pass
    if val == ' ':
        val = None
    return val


def get_obs(awc, lat_min, lon_min, inc, timeback):
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=true'
    url += '&minLon='+str(lon_min)
    url += '&maxLon='+str(min(180, lon_min+inc+1))
    url += '&minLat='+str(lat_min)
    url += '&maxLat='+str(min(90, lat_min+inc+1))
    url += '&hoursBeforeNow='+str(timeback)

    try:
        xml = urllib.request.urlopen(url).read()
        tree = ET.fromstring(xml)
        obs = tree.find('data')
        for ob in obs:
            message = dict()
            for key in keys_main:
                try:
                    message[key] = convert(ob.find(key).text)
                except:
                    pass
            for key in keys_qc:
                try:
                    message['qc_' +
                            key] = convert(ob.find('quality_control_flags').find(key).text)
                except:
                    pass
            for idx, sc in enumerate(ob.findall('sky_condition')):
                for key in keys_sc:
                    try:
                        message[key+'_'+str(idx)] = convert(sc.attrib[key])
                    except:
                        pass
            message['observation_time'] = pd.to_datetime(
                message['observation_time'])
            message['timestamp'] = datetime.utcnow()
            message['topic'] = 'wx/awc'
            message['ttl'] = datetime.utcnow()
            try:
                awc.replace_one(
                    {'station_id': message['station_id']}, message, upsert=True)
                print(message)
            except:
                print('write failed')
    except:
        print('fetch failed')

def get_awc(timeback, inc, max_pool):
    client = MongoClient(
        'mongodb+srv://kk6gpv:ObqL7MKu4IrEvgyE@cluster0-li5mj.gcp.mongodb.net/test?retryWrites=true', maxPoolSize=max_pool)
    db = client.wx
    awc = db.awc
    for lat_min in range(-90, 90, inc):
        for lon_min in range(-180, 180, inc):
            get_obs(awc, lat_min, lon_min, inc, timeback)
    client.close()
    print('got '+str(timeback)+' hours back at '+str(inc)+' deg incs')


def truncate_table():
    client = MongoClient(
        'mongodb+srv://kk6gpv:ObqL7MKu4IrEvgyE@cluster0-li5mj.gcp.mongodb.net/test?retryWrites=true', maxPoolSize=1)
    db = client.wx
    awc = db.awc
    awc.delete_many({})
    client.close()
    print('table truncated')