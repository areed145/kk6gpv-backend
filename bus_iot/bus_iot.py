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
import json
from datetime import datetime
import os


def on_connect(client, userdata, flags, rc):
    print('Connected with result code'+str(rc))
    client.subscribe('eventstream/raw')


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    message = json.loads(message)
    ins = message['event_data']['new_state']
    msg = {}
    msg['type'] = 'iot'
    msg['timestamp'] = datetime.utcnow().isoformat()
    msg['sensor'] = ins['entity_id']
    msg['state'] = ins['state']
    msg['uom'] = ins['attributes']['unit_of_measurement']
    try:
        client.publish('kk6gpv_bus', json.dumps(msg))
    except:
        pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('broker.hivemq.com', 1883, 60)

client.loop_forever()
