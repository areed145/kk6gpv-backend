#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 18:23:20 2019

@author: areed145
"""

import dns
import aprslib
from datetime import datetime
from pymongo import MongoClient
import threading
#import logger

client = MongoClient(
    'mongodb+srv://kk6gpv:ObqL7MKu4IrEvgyE@cluster0-li5mj.gcp.mongodb.net/test?retryWrites=true')
db = client.aprs
raw = db.raw


def unpack_dict_prefix(d):
    try:
        message = dict()
        message['timestamp_'] = datetime.utcnow()
        message['script'] = 'prefix'
        for k, v in d.items():
            try:
                for k1, v1 in v.items():
                    message[k+'_'+k1] = v1
            except:
                try:
                    message[k] = v
                except:
                    message[k] = str(v)
        raw.insert_one(message)
        print(message)
    except:
        print('unpack failed')


def unpack_dict_entry(d):
    try:
        message = dict()
        message['timestamp_'] = datetime.utcnow()
        message['script'] = 'entry'
        for k, v in d.items():
            try:
                for k1, v1 in v.items():
                    message[k+'_'+k1] = v1
            except:
                try:
                    message[k] = v
                except:
                    message[k] = str(v)
        raw.insert_one(message)
        print(message)
    except:
        print('unpack failed')


def unpack_dict_radius(d):
    try:
        message = dict()
        message['timestamp_'] = datetime.utcnow()
        message['ttl'] = datetime.utcnow()
        message['script'] = 'radius'
        for k, v in d.items():
            try:
                for k1, v1 in v.items():
                    message[k+'_'+k1] = v1
            except:
                try:
                    message[k] = v
                except:
                    message[k] = str(v)
        raw.insert_one(message)
        print(message)
    except:
        raw.insert_one(message)
        print('unpack failed')


def consumer(script):
    """Start consumer function for thread
    keyword arguments:
    conn -- APRS-IS connection from aprslib
    """

    #logger.debug("starting consumer thread")

    ais = aprslib.IS('N0CALL', '13023', port=14580)
    ais.connect(blocking=True)

    # Obtain raw APRS-IS packets and sent to callback when received
    if script == 'radius':
        ais.set_filter('r/30/-95/250 t/n')
        ais.consumer(unpack_dict_radius, immortal=True, raw=False)
    if script == 'prefix':
        ais.set_filter('p/KK6GPV')
        ais.consumer(unpack_dict_prefix, immortal=True, raw=False)
    if script == 'entry':
        ais.set_filter('e/KK6GPV*')
        ais.consumer(unpack_dict_entry, immortal=True, raw=False)


def run():
    t1 = threading.Thread(target=consumer, args=('prefix',))
    t2 = threading.Thread(target=consumer, args=('entry',))
    t3 = threading.Thread(target=consumer, args=('radius',))

    t1.start()
    t2.start()
    t3.start()
