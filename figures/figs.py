import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly
import plotly.graph_objs as go
import json

client = MongoClient(
    'mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')

cs = [
    [0.0, '#424ded'],
    [0.1, '#4283ed'],
    [0.2, '#42d0ed'],
    [0.3, '#42edae'],
    [0.4, '#78ed42'],
    [0.5, '#d6ed42'],
    [0.6, '#edde42'],
    [0.7, '#f4af41'],
    [0.8, '#f48541'],
    [0.9, '#f44741'],
    [1.0, '#f44298']
]


def create_plot(feature):
    if feature == 'bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'],  # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x=random_x,
            y=random_y,
            mode='markers'
        )]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_plot2(type, prop, time):
    time = int(time[2:])
    if type == 'prefix':
        N = time
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'],  # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = time
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x=random_x,
            y=random_y,
            mode='markers'
        )]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_graph_iot(sensor, time):
    time = int(time[2:])
    db = client.iot
    df = pd.DataFrame(
        list(db.raw.find({'entity_id': sensor}).sort([('_id', -1)]).limit(time)))
    data = [go.Scatter(x=df['last_changed'],
                       y=df['state'],
                       name=df['entity_id'][0],
                       line=dict(  # color = 'rgb(255, 95, 63)',
        shape='vh',
        width=3),
        mode='lines')]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_map_aprs(script, prop, time):
    params = {'none': [0, 0, 0, ''],
              'altitude': [0, 1000, 3.2808, 'ft'],
              'speed': [0, 100, 0.621371, 'mph'],
              'course': [0, 359, 1, 'degrees'], }

    time = int(time[2:])
    client = MongoClient(
        'mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.aprs
    if script == 'prefix':
        df = pd.DataFrame(list(db.raw.find({'script': script, 'from': 'KK6GPV', 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    else:
        df = pd.DataFrame(list(db.raw.find({'script': script, 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    df = df[['timestamp_', 'latitude', 'longitude',
             'script', 'altitude', 'speed', 'course', 'raw']]
    mapbox_access_token = 'pk.eyJ1IjoiYXJlZWQxNDUiLCJhIjoiY2phdzNsN2ZoMGh0bjMybzF3cTkycWYyciJ9.4aS7z-guI2VDlP3duMg2FA'
    if prop == 'none':
        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw'],
                                 mode='markers',
                                 marker=dict(size=10)
                                 )
                ]
    else:
        if prop == 'course':
            cmin = 0
            cmax = 359
        else:
            cmin = df[prop].quantile(0.01)
            cmax = df[prop].quantile(0.99)
        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw'],
                                 mode='markers',
                                 marker=dict(size=10,
                                             color=params[prop][2] *
                                             df[prop],
                                             colorbar=dict(
                                                 title=params[prop][3]),
                                             colorscale=cs,
                                             cmin=cmin,
                                             cmax=cmax,
                                             )
                                 )
                ]
    layout = go.Layout(autosize=True,
                       # height=1000,
                       showlegend=False,
                       hovermode='closest',
                       uirevision=True,
                       margin=dict(r=0, t=0, b=0, l=0, pad=0),
                       mapbox=dict(bearing=0,
                                   center=dict(lat=30, lon=-95),
                                   accesstoken=mapbox_access_token,
                                   style='satellite-streets',
                                   pitch=0,
                                   zoom=6
                                   )
                       )
    graphJSON = json.dumps(dict(data=data, layout=layout),
                           cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
