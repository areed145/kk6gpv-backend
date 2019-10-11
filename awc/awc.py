#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 20:36:47 2019

@author: areed145
"""

import dns
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np
import time
#from multiprocessing import Pool

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


def get_range(message, rad, awc, prop):
    r = 2
    lat = message['latitude']
    lon = message['longitude']
    #elev = message['elevation_m']
    #val = message[prop]
    df = pd.DataFrame(list(awc.find({'latitude': {'$gt': lat-r}, 'latitude': {
                      '$lt': lat+r}, 'longitude': {'$gt': lon-r}, 'longitude': {'$lt': lon+r}})))
    df['dist'] = np.arccos(np.sin(lat*np.pi/180) * np.sin(df['latitude']*np.pi/180) + np.cos(lat*np.pi/180) * np.cos(df['latitude']*np.pi/180) * np.cos((df['longitude']*np.pi/180) - (lon*np.pi/180))) * 6371 
    df = df[df['dist'] <= rad]
    #df['r2'] = df[prop] * df['elevation_m']
    #df['dPe'] = df['r2'] - (val * elev)
    if len(df) >= 3:
        df = df[(df[prop] < df[prop].quantile(0.99)) & (df[prop] > df[prop].quantile(0.01))]
    return df[prop].max() - df[prop].min()


def get_obs(lat_min, lon_min, inc, timeback, max_pool):
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=true'
    url += '&minLon='+str(lon_min)
    url += '&maxLon='+str(min(180, lon_min+inc+1))
    url += '&minLat='+str(lat_min)
    url += '&maxLat='+str(min(90, lat_min+inc+1))
    url += '&hoursBeforeNow='+str(timeback)

    client = MongoClient('mongodb://kk6gpv:kk6gpv@mongo-mongodb-replicaset-0.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-1.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-2.mongo-mongodb-replicaset.default.svc.cluster.local/?replicaSet=db')
    db = client.wx
    awc = db.awc

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
            message['temp_c_range'] = get_range(message, 150, awc, 'temp_c')
            message['altim_in_hg_range'] = get_range(message, 250, awc, 'altim_in_hg')
            try:
                # awc.insert_one(message)
                awc.replace_one(
                    {'station_id': message['station_id']}, message, upsert=True)
                print(message)
            except:
                print('duplicate post')
    except:
        print('failed')


if __name__ == '__main__':
    last_hour = datetime.now().hour - 1
    last_minute = datetime.now().minute - 1
    while True:
        if datetime.now().hour != last_hour:
            #pl = Pool(48)
            inc = 15
            for lat_min in range(-90, 90, inc):
                for lon_min in range(-180, 180, inc):
                    #pl.apply_async(get_obs, args=(lat_min, lon_min, inc, 1, 2))
                    get_obs(lat_min, lon_min, inc, 1, 2)
            # pl.close()
            # pl.join()
            last_hour = datetime.now().hour
            print('got long')
        elif datetime.now().minute != last_minute:
            #ps = Pool(32)
            inc = 45
            for lat_min in range(-90, 90, inc):
                for lon_min in range(-180, 180, inc):
                    #ps.apply_async(get_obs, args=(lat_min, lon_min, inc, 0.02, 3))
                    get_obs(lat_min, lon_min, inc, 0.02, 3)
            # ps.close()
            # ps.join()
            last_minute = datetime.now().minute
            print('got short')
        else:
            print('skipping updates')
        time.sleep(10)
