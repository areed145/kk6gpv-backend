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
import os


def unpack_dict(d):
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


if __name__ == '__main__':
    while True:
        try:
            # MongoDB client
            client = MongoClient(os.environ['MONGODB_CLIENT'])
            db = client.aprs
            raw = db.raw

            # Mosquitto client
            ais = aprslib.IS('N0CALL', '13023', port=14580)
            ais.set_filter('e/KK6GPV*')
            ais.connect()
            ais.consumer(unpack_dict, raw=False)
        except:
            pass
