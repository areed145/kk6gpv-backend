#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 18:23:20 2019

@author: areed145
"""

import dns
import aprslib
from datetime import datetime
import paho.mqtt.client as mqtt
import os
import json
import sys


def unpack_dict(d):
    try:
        message = {}
        message['timestamp'] = datetime.utcnow().isoformat()
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
        client.publish(
            'kk6gpv_bus/aprs/' + str(message['script']),
            json.dumps(message),
            retain=True
        )
        print(message)
    except:
        print('unpack failed')


if __name__ == '__main__':
    while True:
        try:
            client = mqtt.Client(
                client_id='l', clean_session=True, userdata=None)
            client.connect('broker.mqttdashboard.com', 1883)

            ais = aprslib.IS('N0CALL', '13023', port=14580)
            ais.set_filter('r/30/-95/50 t/n')
            ais.connect()
            ais.consumer(unpack_dict, raw=False)
        except:
            pass
