import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly
import plotly.graph_objs as go
import json

client = MongoClient(
    'mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')

mapbox_access_token = 'pk.eyJ1IjoiYXJlZWQxNDUiLCJhIjoiY2phdzNsN2ZoMGh0bjMybzF3cTkycWYyciJ9.4aS7z-guI2VDlP3duMg2FA'

cs_normal = [
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

cs_rdgn = [
    [0.0, '#f44741'],
    [0.2, '#f48541'],
    [0.4, '#f4af41'],
    [0.6, '#edde42'],
    [0.8, '#d6ed42'],
    [1.0, '#78ed42']
]

cs_circle = [
    [0.000, '#f45f42'],
    [0.067, '#f7856f'],
    [0.133, '#e2aba1'],
    [0.200, '#d8bdb8'],
    [0.267, '#BCBCBC'],
    [0.333, '#bac8e0'],
    [0.400, '#aeccfc'],
    [0.467, '#77aaf9'],
    [0.533, '#4186f4'],
    [0.600, '#77aaf9'],
    [0.667, '#aeccfc'],
    [0.733, '#bac8e0'],
    [0.800, '#BCBCBC'],
    [0.867, '#d8bdb8'],
    [0.933, '#e2aba1'],
    [1.000, '#f7856f'],
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


def create_map_awc(prop):
    params = {'flight_category': [0, 0, 0, ''],
              'temp_c': [0, 100, 1, 'C'],
              'dewpoint_c': [0, 100, 1, 'C'],
              'altim_in_hg': [0, 100, 1, 'inHg'],
              'wind_dir_degrees': [0, 359, 1, 'degrees'],
              'wind_speed_kt': [0, 100, 1, 'kts'],
              'wind_gust_kt': [0, 100, 1, 'kts'],
              'visibility_statute_mi': [0, 100, 1, 'mi'],
              'cloud_base_ft_agl_0': [0, 10000, 1, 'ft'],
              'sky_cover_0': [0, 100, 1, 'degrees'],
              'precip_in': [0, 10, 1, 'degrees'],
              'elevation_m': [0, 10000, 3.2808, 'ft'], }

    db = client.wx

    df = pd.DataFrame(list(db.awc.find()))

    if prop == 'flight_category':
        df_vfr = df[df['flight_category'] == 'VFR']
        df_mvfr = df[df['flight_category'] == 'MVFR']
        df_ifr = df[df['flight_category'] == 'IFR']
        df_lifr = df[df['flight_category'] == 'LIFR']

        data = [go.Scattermapbox(lat=df_vfr['latitude'],
                                 lon=df_vfr['longitude'],
                                 text=df_vfr['raw_text'],
                                 mode='markers',
                                 name='VFR',
                                 marker=dict(size=10,
                                             color='rgb(0,255,0)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_mvfr['latitude'],
                                 lon=df_mvfr['longitude'],
                                 text=df_mvfr['raw_text'],
                                 mode='markers',
                                 name='MVFR',
                                 marker=dict(size=10,
                                             color='rgb(0,0,255)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_ifr['latitude'],
                                 lon=df_ifr['longitude'],
                                 text=df_ifr['raw_text'],
                                 mode='markers',
                                 name='IFR',
                                 marker=dict(size=10,
                                             color='rgb(255,0,0)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_lifr['latitude'],
                                 lon=df_lifr['longitude'],
                                 text=df_lifr['raw_text'],
                                 mode='markers',
                                 name='LIFR',
                                 marker=dict(size=10,
                                             color='rgb(255,127.5,255)',
                                             )
                                 )
                ]
    elif prop == 'sky_cover_0':
        df_clr = df[df['sky_cover_0'] == 'CLR']
        df_few = df[df['sky_cover_0'] == 'FEW']
        df_sct = df[df['sky_cover_0'] == 'SCT']
        df_bkn = df[df['sky_cover_0'] == 'BKN']
        df_ovc = df[df['sky_cover_0'] == 'OVC']
        df_ovx = df[df['sky_cover_0'] == 'OVX']

        data = [go.Scattermapbox(lat=df_clr['latitude'],
                                 lon=df_clr['longitude'],
                                 text=df_clr['raw_text'],
                                 mode='markers',
                                 name='CLR',
                                 marker=dict(size=10,
                                             color='rgb(21, 230, 234)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_few['latitude'],
                                 lon=df_few['longitude'],
                                 text=df_few['raw_text'],
                                 mode='markers',
                                 name='FEW',
                                 marker=dict(size=10,
                                             color='rgb(194, 234, 21)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_sct['latitude'],
                                 lon=df_sct['longitude'],
                                 text=df_sct['raw_text'],
                                 mode='markers',
                                 name='SCT',
                                 marker=dict(size=10,
                                             color='rgb(234, 216, 21)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_bkn['latitude'],
                                 lon=df_bkn['longitude'],
                                 text=df_bkn['raw_text'],
                                 mode='markers',
                                 name='BKN',
                                 marker=dict(size=10,
                                             color='rgb(234, 181, 21)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_ovc['latitude'],
                                 lon=df_ovc['longitude'],
                                 text=df_ovc['raw_text'],
                                 mode='markers',
                                 name='OVC',
                                 marker=dict(size=10,
                                             color='rgb(234, 77, 21)',
                                             )
                                 ),
                go.Scattermapbox(lat=df_ovx['latitude'],
                                 lon=df_ovx['longitude'],
                                 text=df_ovx['raw_text'],
                                 mode='markers',
                                 name='OVX',
                                 marker=dict(size=10,
                                             color='rgb(234, 21, 21)',
                                             )
                                 )
                ]
    else:
        cs = cs_normal
        if prop == '':
            cmin = 0
            cmax = 359
            cs = cs_circle
        else:
            cmin = df[prop].quantile(0.01)
            cmax = df[prop].quantile(0.99)
        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw_text'],
                                 mode='markers',
                                 marker=dict(size=10,
                                             color=params[prop][2] * df[prop],
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
                                   center=dict(lat=38, lon=-96),
                                   accesstoken=mapbox_access_token,
                                   style='satellite-streets',
                                   pitch=0,
                                   zoom=3
                                   )
                       )
    graphJSON = json.dumps(dict(data=data, layout=layout),
                           cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_map_aprs(script, prop, time):
    params = {'none': [0, 0, 0, ''],
              'altitude': [0, 1000, 3.2808, 'ft'],
              'speed': [0, 100, 0.621371, 'mph'],
              'course': [0, 359, 1, 'degrees'], }

    time = int(time[2:])
    db = client.aprs
    if script == 'prefix':
        df = pd.DataFrame(list(db.raw.find({'script': script, 'from': 'KK6GPV', 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    else:
        df = pd.DataFrame(list(db.raw.find({'script': script, 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    df = df[['timestamp_', 'latitude', 'longitude',
             'script', 'altitude', 'speed', 'course', 'raw']]
    if prop == 'none':
        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw'],
                                 mode='markers',
                                 marker=dict(size=10)
                                 )
                ]
    else:
        cs = cs_normal
        if prop == 'course':
            cmin = 0
            cmax = 359
            cs = cs_circle
        else:
            cmin = df[prop].quantile(0.01)
            cmax = df[prop].quantile(0.99)
        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw'],
                                 mode='markers',
                                 marker=dict(size=10,
                                             color=params[prop][2] * df[prop],
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
