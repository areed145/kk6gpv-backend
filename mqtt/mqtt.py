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


def on_connect(client, userdata, flags, rc):
    print('Connected with result code'+str(rc))
    client.subscribe('eventstream/raw')


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    message = json.loads(message)
    ins = message['event_data']['new_state']
    ins['timestamp_'] = datetime.utcnow()
    try:
        raw.insert_one(ins)
        # print(message)
    except:
        pass
        # print('failed')


# MongoDB client
client = MongoClient('mongodb://kk6gpv:kk6gpv@mongo-mongodb-replicaset-0.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-1.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-2.mongo-mongodb-replicaset.default.svc.cluster.local/?replicaSet=db')
db = client.iot
raw = db.raw

# Mosquitto client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('broker.hivemq.com', 1883, 60)
client.loop_forever()
