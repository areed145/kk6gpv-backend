#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 18:23:20 2019

@author: areed145
"""

import dns
import ast
import paho.mqtt.client as mqtt
from datetime import datetime
from pymongo import MongoClient

def fix_keys(d):
    for key in d.keys():
        d[key.replace('.','_')] = d.pop(key)

def on_connect(client, userdata, flags, rc):
    print('Connected with result code'+str(rc))
    client.subscribe('iot/vib')

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    message = ast.literal_eval(message)
    message['timestamp'] = datetime.utcnow()
    message['topic'] = "iot/vib"
    try:
        #fix_keys(message)
        vib.insert_one(message)
        print(message)
    except:
        print('failed')

if __name__ == '__main__':
    # MongoDB client
    client=MongoClient('mongodb+srv://kk6gpv:ObqL7MKu4IrEvgyE@cluster0-li5mj.gcp.mongodb.net/test?retryWrites=true')
    db=client.iot
    vib=db.vib

    # Mosquitto client
    mos = mqtt.Client()
    mos.on_connect = on_connect
    mos.on_message = on_message
    mos.connect('159.89.146.242', 1883, 60)
    mos.loop_forever()