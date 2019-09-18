import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime

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

cs_gnrd = [
    [0.0, '#78ed42'],
    [0.2, '#d6ed42'],
    [0.4, '#edde42'],
    [0.6, '#f4af41'],
    [0.8, '#f48541'],
    [1.0, '#f44741'],
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
    params = {'flight_category': [0, 0, 0, 0, ''],
              'temp_c': [0, 100, 1.8, 32, 'F'],
              'dewpoint_c': [0, 100, 1.8, 32, 'F'],
              'temp_dewpoint_spread': [0, 100, 1.8, 0, 'F'],
              'altim_in_hg': [0, 100, 1, 0, 'inHg'],
              'wind_dir_degrees': [0, 359, 1, 0, 'degrees'],
              'wind_speed_kt': [0, 100, 1, 0, 'kts'],
              'wind_gust_kt': [0, 100, 1, 0, 'kts'],
              'visibility_statute_mi': [0, 100, 1, 0, 'mi'],
              'cloud_base_ft_agl_0': [0, 10000, 1, 0, 'ft'],
              'sky_cover_0': [0, 100, 1, 0, 'degrees'],
              'precip_in': [0, 10, 1, 0, 'degrees'],
              'elevation_m': [0, 10000, 3.2808, 0, 'ft'],
              'age': [0, 10000, 1, 0, 'minutes'],
              'three_hr_pressure_tendency_mb': [0, 10000, 1, 0, '?'],
              }

    db = client.wx

    df = pd.DataFrame(list(db.awc.find()))

    legend = False

    if prop == 'flight_category':
        df_vfr = df[df['flight_category'] == 'VFR']
        df_mvfr = df[df['flight_category'] == 'MVFR']
        df_ifr = df[df['flight_category'] == 'IFR']
        df_lifr = df[df['flight_category'] == 'LIFR']
        legend = True

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
        legend = True

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
        if prop == 'wind_dir_degrees':
            cs = cs_circle
            cmin = 0
            cmax = 359
        elif prop == 'visibility_statute_mi':
            cs = cs_rdgn
            cmin = 0
            cmax = 10
        elif prop == 'cloud_base_ft_agl_0':
            cs = cs_rdgn
            cmin = 0
            cmax = 2000
        elif prop == 'age':
            df['age'] = (datetime.utcnow() - df['observation_time']
                         ).astype('timedelta64[m]')
            cs = cs_gnrd
            cmin = 0
            cmax = 60
        elif prop == 'temp_dewpoint_spread':
            df['temp_dewpoint_spread'] = df['temp_c'] - df['dewpoint_c']
            cs = cs_rdgn
            cmin = 0
            cmax = 5
        else:
            cs = cs_normal
            cmin = df[prop].quantile(0.01)
            cmax = df[prop].quantile(0.99)

        data = [go.Scattermapbox(lat=df['latitude'],
                                 lon=df['longitude'],
                                 text=df['raw_text'],
                                 mode='markers',
                                 marker=dict(size=10,
                                             color=params[prop][2] *
                                             df[prop] + params[prop][3],
                                             colorbar=dict(
                                                 title=params[prop][4]),
                                             colorscale=cs,
                                             cmin=params[prop][2] *
                                             cmin + params[prop][3],
                                             cmax=params[prop][2] *
                                             cmax + params[prop][3],
                                             )
                                 )
                ]
    layout = go.Layout(autosize=True,
                       # height=1000,
                       showlegend=legend,
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
    params = {'none': [0, 0, 0, 0, ''],
              'altitude': [0, 1000, 3.2808, 0, 'ft'],
              'speed': [0, 100, 0.621371, 0, 'mph'],
              'course': [0, 359, 1, 0, 'degrees'], }

    time = int(time[2:])
    db = client.aprs
    if script == 'prefix':
        df = pd.DataFrame(list(db.raw.find({'script': script, 'from': 'KK6GPV', 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    else:
        df = pd.DataFrame(list(db.raw.find({'script': script, 'latitude': {
                          '$exists': True, '$ne': None}}).sort([('timestamp_', -1)]).limit(time)))
    # df = df[['timestamp_', 'latitude', 'longitude',
    #          'script', 'altitude', 'speed', 'course', 'raw']]
    if prop == 'none':
        data_map = [go.Scattermapbox(lat=df['latitude'],
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
        data_map = [go.Scattermapbox(lat=df['latitude'],
                                     lon=df['longitude'],
                                     text=df['raw'],
                                     mode='markers',
                                     marker=dict(size=10,
                                                 color=params[prop][2] *
                                                 df[prop] + params[prop][3],
                                                 colorbar=dict(
                                                     title=params[prop][4]),
                                                 colorscale=cs,
                                                 cmin=params[prop][2] *
                                                 cmin + params[prop][3],
                                                 cmax=params[prop][2] *
                                                 cmax + params[prop][3],
                                                 )
                                     )
                    ]
    layout_map = go.Layout(autosize=True,
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

    data_speed = [
        go.Scatter(x=df['timestamp_'],
                   y=df['speed'],
                   name='Speed (mph)',
                   line=dict(color='rgb(255, 127, 63)',
                             width=2, shape='linear'),
                   # xaxis='x', yaxis='y',
                   mode='lines'),
    ]

    layout_speed = go.Layout(autosize=True,
                             height=200,
                             yaxis=dict(domain=[0.02, 0.98],
                                        title='Speed (mph)',
                                        # range=[td_min,td_max],
                                        fixedrange=True,
                                        titlefont=dict(
                                            color='rgb(255, 95, 63)')
                                        ),
                             xaxis=dict(type='date', fixedrange=False),
                             margin=dict(r=50, t=30, b=30, l=60, pad=0),
                             showlegend=False,
                             )

    data_alt = [
        go.Scatter(x=df['timestamp_'],
                   y=df['altitude'],
                   name='Altitude (ft)',
                   line=dict(color='rgb(255, 95, 63)',
                             width=2, shape='linear'),
                   # xaxis='x', yaxis='y',
                   mode='lines'),
    ]

    layout_alt = go.Layout(autosize=True,
                           height=200,
                           yaxis=dict(domain=[0.02, 0.98],
                                      title='Altitude (ft)',
                                      # range=[td_min,td_max],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(255, 95, 63)')
                                      ),
                           xaxis=dict(type='date', fixedrange=False),
                           margin=dict(r=50, t=30, b=30, l=60, pad=0),
                           showlegend=False,
                           )

    data_course = [
        go.Scatter(x=df['timestamp_'],
                   y=df['course'],
                   name='Course (degrees)',
                   line=dict(color='rgb(255, 63, 63)',
                             width=2, shape='linear'),
                   # xaxis='x', yaxis='y',
                   mode='lines'),
    ]

    layout_course = go.Layout(autosize=True,
                              height=200,
                              yaxis=dict(domain=[0.02, 0.98],
                                         title='Course (degrees)',
                                         # range=[td_min,td_max],
                                         fixedrange=True,
                                         titlefont=dict(
                                             color='rgb(255, 95, 63)')
                                         ),
                              xaxis=dict(type='date', fixedrange=False),
                              margin=dict(r=50, t=30, b=30, l=60, pad=0),
                              showlegend=False,
                              )

    graphJSON_map = json.dumps(dict(data=data_map, layout=layout_map),
                               cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_speed = json.dumps(dict(data=data_speed, layout=layout_speed),
                                 cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_alt = json.dumps(dict(data=data_alt, layout=layout_alt),
                               cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_course = json.dumps(dict(data=data_course, layout=layout_course),
                                  cls=plotly.utils.PlotlyJSONEncoder)

    df['timestamp_'] = df['timestamp_'].apply(
        lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    rows = []
    for _, row in df.iterrows():
        r = {}
        r['timestamp_'] = row['timestamp_']
        r['from'] = row['from']
        r['to'] = row['to']
        r['latitude'] = np.round(row['latitude'], 3)
        r['longitude'] = np.round(row['longitude'], 3)
        r['speed'] = np.round(row['speed'], 2)
        r['altitude'] = np.round(row['altitude'], 2)
        r['course'] = np.round(row['course'], 0)
        rows.append(r)
    print(rows)

    return graphJSON_map, graphJSON_speed, graphJSON_alt, graphJSON_course, rows
