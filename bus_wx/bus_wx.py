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
import json
import os
import asyncio
import websockets
import numpy as np


async def wx_connect(ws):
    await ws.send('{"type":"listen_start", "device_id":54051, "id": "2098388936"}')
    await ws.send('{"type":"listen_start", "device_id":54053, "id": "2098388936"}')
    await ws.send('{"type":"listen_rapid_start", "device_id":54053, "id": "2098388936"}')


async def wx_on_message(ws):
    while True:
        message = await ws.recv()
        message = json.loads(message)
        if message['type'] == "obs_air":
            msg = {}
            msg['type'] = 'wx_air'
            msg['temp_f'] = str(np.round(
                (message['obs'][0][2] * (9 / 5) + 32), 2))
            msg['dewpoint_f'] = str(np.round(
                (message['obs'][0][2] - (100 - message['obs'][0][3]) / 5) * (9 / 5) + 32, 2))
            msg['relative_humidity'] = str(np.round(
                message['obs'][0][3], 2))
            msg['pressure_in'] = str(np.round(
                message['obs'][0][1] * 0.029693, 3))
            msg['pressure_trend'] = str(
                message['summary']['pressure_trend'])
            msg['strike_count_3h'] = str(
                message['summary']['strike_count_3h'])
            msg['strike_last_dist'] = str(
                message['summary']['strike_last_dist'])
            msg['strike_last_epoch'] = str(
                message['summary']['strike_last_epoch'])
            msg['feels_like'] = str(message['summary']['feels_like'])
            msg['heat_index'] = str(message['summary']['heat_index'])
            msg['wind_chill'] = str(message['summary']['wind_chill'])

        if message['type'] == "obs_sky":
            msg = {}
            msg['type'] = 'wx_sky'
            msg['wind_degrees'] = str(message['obs'][0][7])
            msg['wind_mph'] = str(np.round(
                message['obs'][0][5] * 1.94384, 2))
            msg['wind_gust_mph'] = str(np.round(
                message['obs'][0][6] * 1.94384, 2))
            msg['precip_today_in'] = str(np.round(
                message['obs'][0][11] * 0.0393701, 3))
            msg['solar_radiation'] = str(message['obs'][0][10])
            msg['uv'] = str(message['obs'][0][2])
            msg['wind_degrees'] = str(message['obs'][0][7])

        if message['type'] == "rapid_wind":
            msg = {}
            msg['type'] = 'wx_wind'
            msg['wind_degrees'] = str(message['ob'][2])
            msg['wind_mph'] = str(np.round(message['ob'][1] * 1.94384, 2))

        try:
            client.publish('kk6gpv_bus', json.dumps(msg))
        except:
            pass


async def weatherstation():
    uri = "wss://ws.weatherflow.com/swd/data?api_key=20c70eae-e62f-4d3b-b3a4-8586e90f3ac8"
    async with websockets.connect(uri) as ws:
        await wx_connect(ws)
        await wx_on_message(ws)

client = mqtt.Client()
client.connect('broker.hivemq.com', 1883, 60)

asyncio.get_event_loop().run_until_complete(weatherstation())
