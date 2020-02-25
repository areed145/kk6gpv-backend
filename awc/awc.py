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
import os
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


client = MongoClient(os.environ['MONGODB_CLIENT'])
db = client.wx
awc = db.awc
df_running = pd.DataFrame(awc.find({}))


def get_var(message, rad, prop):
    r = rad/50
    lat = message['latitude']
    lon = message['longitude']

    df = df_running[
        (df_running['latitude'] > lat-r) &
        (df_running['latitude'] < lat+r) &
        (df_running['longitude'] > lon-r) &
        (df_running['longitude'] < lon+r)
    ]

    df['dist'] = np.arccos(np.sin(lat*np.pi/180) * np.sin(df['latitude']*np.pi/180) + np.cos(lat*np.pi/180)
                           * np.cos(df['latitude']*np.pi/180) * np.cos((df['longitude']*np.pi/180) - (lon*np.pi/180))) * 6371
    df = df[df['dist'] <= rad]
    if len(df) >= 3:
        df = df[(df[prop] < df[prop].quantile(0.99)) &
                (df[prop] > df[prop].quantile(0.01))]
    return df[prop].std()


def get_prev(message, awc):

    df = df_running[
        df_running['station_id'] == message['station_id']
    ]
    return df


def get_obs(lat_min, lon_min, inc, timeback, max_pool):
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=true'
    url += '&minLon='+str(lon_min)
    url += '&maxLon='+str(min(180, lon_min+inc+1))
    url += '&minLat='+str(lat_min)
    url += '&maxLat='+str(min(90, lat_min+inc+1))
    url += '&hoursBeforeNow='+str(timeback)

    client = MongoClient(os.environ['MONGODB_CLIENT'])
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
                message['observation_time'], utc=True)
            try:
                prev = get_prev(message, awc)
                prev.reset_index(inplace=True)
                prev['observation_time'] = pd.to_datetime(
                    prev['observation_time'], utc=True)
                if message['observation_time'] > prev['observation_time'][0]:
                    message['timestamp'] = datetime.utcnow()
                    message['topic'] = 'wx/awc'
                    message['ttl'] = datetime.utcnow()
                    message['temp_c_var'] = get_var(
                        message, 150, 'temp_c')
                    message['altim_in_hg_var'] = get_var(
                        message, 250, 'altim_in_hg')
                    for col in ['temp_c', 'dewpoint_c', 'altim_in_hg', 'wind_speed_kt', 'wind_gust_kt', 'cloud_base_ft_agl_0']:
                        try:
                            message[col+'_delta'] = message[col] - prev[col][0]
                        except:
                            pass
                    try:
                        awc.replace_one(
                            {'station_id': message['station_id']}, message, upsert=True)
                        for key in message:
                            df_running.loc[df_running['station_id'] ==
                                           message['station_id'], key] = message[key]
                        print(message)
                    except:
                        print('error')
                else:
                    print('duplicate post')
            except:
                print('first station post')
                message['timestamp'] = datetime.utcnow()
                message['topic'] = 'wx/awc'
                message['ttl'] = datetime.utcnow()
                try:
                    awc.replace_one(
                        {'station_id': message['station_id']}, message, upsert=True)
                    for key in message:
                        df_running.loc[df_running['station_id'] ==
                                       message['station_id'], key] = message[key]
                    print(message)
                except:
                    print('error')

    except:
        print('failed')


if __name__ == '__main__':
    last_hour = datetime.now().hour - 1
    last_minute = datetime.now().minute - 1
    while True:
        if datetime.now().hour != last_hour:
            #pl = Pool(48)
            inc = 10
            for lat_min in range(-90, 90, inc):
                for lon_min in range(-180, 180, inc):
                    #pl.apply_async(get_obs, args=(lat_min, lon_min, inc, 1, 2))
                    get_obs(lat_min, lon_min, inc, 1.1, 3)
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
