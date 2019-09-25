import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime

#client = MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
client = MongoClient('mongodb://kk6gpv:kk6gpv@mongo-mongodb-replicaset-0.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-1.mongo-mongodb-replicaset.default.svc.cluster.local,mongo-mongodb-replicaset-2.mongo-mongodb-replicaset.default.svc.cluster.local/?replicaSet=db')
# client = MongoClient('mongodb://localhost:27017/',
#                      username='kk6gpv', password='kk6gpv', authSource='admin')


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
        data = [go.Scattergl(
            x=random_x,
            y=random_y,
            mode='markers'
        )]
    layout = go.Layout(autosize=True,
                       # height=1000,
                       #    showlegend=True,
                       hovermode='closest',
                       uirevision=True,
                       margin=dict(r=0, t=0, b=0, l=0, pad=0),
                       )
    graphJSON = json.dumps(dict(data=data, layout=layout),
                           cls=plotly.utils.PlotlyJSONEncoder)
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
        data = [go.Scattergl(
            x=random_x,
            y=random_y,
            mode='markers'
        )]
    layout = go.Layout(autosize=True,
                       # height=1000,
                       #    showlegend=True,
                       hovermode='closest',
                       uirevision=True,
                       margin=dict(r=0, t=0, b=0, l=0, pad=0),
                       )
    graphJSON = json.dumps(dict(data=data, layout=layout),
                           cls=plotly.utils.PlotlyJSONEncoder)
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

    layout = go.Layout(autosize=True,
                       # height=1000,
                       #    showlegend=True,
                       hovermode='closest',
                       uirevision=True,
                       margin=dict(r=50, t=30, b=30, l=60, pad=0),
                       )
    graphJSON = json.dumps(dict(data=data, layout=layout),
                           cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_map_oilgas():
    db = client.petroleum
    df = pd.DataFrame(list(db.doggr.find({}, {'latitude': 1, 'longitude': 1})))
    data = [go.Scattermapbox(lat=df['latitude'],
                             lon=df['longitude'],
                             #  text=df['raw_text'],
                             mode='markers',
                             #  marker=dict(size=10,
                             #              color=params[prop][2] *
                             #              df[prop] + params[prop][3],
                             #              colorbar=dict(
                             #                  title=params[prop][4]),
                             #              colorscale=cs,
                             #              cmin=params[prop][2] *
                             #              cmin + params[prop][3],
                             #              cmax=params[prop][2] *
                             #              cmax + params[prop][3],
                             #              )
                             )
            ]
    layout = go.Layout(autosize=True,
                       # height=1000,
                       #    showlegend=True,
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
    df['latitude'] = np.round(df['latitude'], 3)
    df['longitude'] = np.round(df['longitude'], 3)
    df['speed'] = np.round(df['speed'], 2)
    df['altitude'] = np.round(df['altitude'], 1)
    df['course'] = np.round(df['course'], 1)
    df = df.fillna('')
    rows = []
    for _, row in df.iterrows():
        r = {}
        r['timestamp_'] = row['timestamp_']
        r['from'] = row['from']
        r['to'] = row['to']
        r['latitude'] = row['latitude']
        r['longitude'] = row['longitude']
        r['speed'] = row['speed']
        r['altitude'] = row['altitude']
        r['course'] = row['course']
        rows.append(r)
    print(rows)

    return graphJSON_map, graphJSON_speed, graphJSON_alt, graphJSON_course, rows


def create_wx_figs(time, sid):
    time = int(time[2:])

    db = client.wx

    df_wx_raw = pd.DataFrame(list(db.raw.find({'station_id': sid}).sort(
        [('observation_time_rfc822', -1)]).limit(time)))
    df_wx_raw.index = df_wx_raw['observation_time_rfc822']
    #df_wx_raw = df_wx_raw.tz_localize('UTC').tz_convert('US/Central')

    for col in df_wx_raw.columns:
        try:
            df_wx_raw.loc[df_wx_raw[col] < -50, col] = pd.np.nan
        except:
            pass

    df_wx_raw['cloudbase'] = (
        (df_wx_raw['temp_f'] - df_wx_raw['dewpoint_f']) / 4.4) * 1000 + 50
    df_wx_raw.loc[df_wx_raw['pressure_in'] < 0, 'pressure_in'] = pd.np.nan

    #df_wx_raw2 = df_wx_raw.resample('5T').mean().interpolate()
    #df_wx_raw2['dat'] = df_wx_raw2.index
    #df_wx_raw2['temp_delta'] = df_wx_raw2.temp_f.diff()
    #df_wx_raw2['precip_today_delta'] = df_wx_raw2.precip_today_in.diff()
    #df_wx_raw2.loc[df_wx_raw2['precip_today_delta'] < 0, 'precip_today_delta'] = 0
    #df_wx_raw2['precip_cum_in'] = df_wx_raw2.precip_today_delta.cumsum()
    #df_wx_raw2['pres_delta'] = df_wx_raw2.pressure_in.diff()
    #df_wx_raw2['dat_delta'] = df_wx_raw2.dat.diff().dt.seconds / 360
    #df_wx_raw2['dTdt'] = df_wx_raw2['temp_delta'] / df_wx_raw2['dat_delta']
    #df_wx_raw2['dPdt'] = df_wx_raw2['pres_delta'] / df_wx_raw2['dat_delta']
    #df_wx_raw3 = df_wx_raw2.drop(columns=['dat'])
    #df_wx_raw3 = df_wx_raw3.rolling(20*3).mean().add_suffix('_roll')
    #df_wx_raw = df_wx_raw2.join(df_wx_raw3)

    df_wx_raw['dat'] = df_wx_raw.index
    df_wx_raw.sort_values(by='dat', inplace=True)
    df_wx_raw['temp_delta'] = df_wx_raw.temp_f.diff()
    df_wx_raw['precip_today_delta'] = df_wx_raw.precip_today_in.diff()
    df_wx_raw.loc[df_wx_raw['precip_today_delta']
                  < 0, 'precip_today_delta'] = 0
    df_wx_raw['precip_cum_in'] = df_wx_raw.precip_today_delta.cumsum()
    df_wx_raw['pres_delta'] = df_wx_raw.pressure_in.diff()
    df_wx_raw['dat_delta'] = df_wx_raw.dat.diff().dt.seconds / 360
    df_wx_raw['dTdt'] = df_wx_raw['temp_delta'] / df_wx_raw['dat_delta']
    df_wx_raw['dPdt'] = df_wx_raw['pres_delta'] / df_wx_raw['dat_delta']

    df_wx_raw['date'] = df_wx_raw.index.date
    df_wx_raw['hour'] = df_wx_raw.index.hour

    df_wx_raw.loc[df_wx_raw['wind_mph'] == 0, 'wind_cat'] = 'calm'
    df_wx_raw.loc[df_wx_raw['wind_mph'] > 0, 'wind_cat'] = '0-1'
    df_wx_raw.loc[df_wx_raw['wind_mph'] > 1, 'wind_cat'] = '1-2'
    df_wx_raw.loc[df_wx_raw['wind_mph'] > 2, 'wind_cat'] = '2-5'
    df_wx_raw.loc[df_wx_raw['wind_mph'] > 5, 'wind_cat'] = '5-10'
    df_wx_raw.loc[df_wx_raw['wind_mph'] > 10, 'wind_cat'] = '>10'

    df_wx_raw['wind_degrees_cat'] = np.floor(
        df_wx_raw['wind_degrees'] / 15) * 15
    df_wx_raw.loc[df_wx_raw['wind_degrees_cat'] == 360, 'wind_degrees_cat'] = 0
    df_wx_raw['wind_degrees_cat'] = df_wx_raw['wind_degrees_cat'].fillna(
        0).astype(int).astype(str)

    df_wx_raw.loc[df_wx_raw['wind_mph'] == 0, 'wind_degrees'] = pd.np.nan

    wind = df_wx_raw[['wind_cat', 'wind_degrees_cat']]
    wind['count'] = 1
    ct = len(wind)
    wind = pd.pivot_table(wind, values='count', index=[
                          'wind_degrees_cat'], columns=['wind_cat'], aggfunc=np.sum)
    ix = np.arange(0, 360, 5)
    col = ['calm', '0-1', '1-2', '2-5', '5-10', '>10']
    wind_temp = pd.DataFrame(data=0, index=ix, columns=col)
    for i in ix:
        for j in col:
            try:
                wind_temp.loc[i, j] = wind.loc[str(i), j]
            except:
                pass
    wind_temp = wind_temp.fillna(0)
    wind_temp['calm'] = wind_temp['calm'].mean()
    for col in range(len(wind_temp.columns)):
        try:
            wind_temp.iloc[:, col] = wind_temp.iloc[:, col] + \
                wind_temp.iloc[:, col-1]
        except:
            pass
    wind_temp = np.round(wind_temp / ct * 100, 2)
    wind_temp['wind_cat'] = wind_temp.index

    dt_min = df_wx_raw.index.min()
    dt_max = df_wx_raw.index.max()

    td_max = max(df_wx_raw['temp_f'].max(), df_wx_raw['dewpoint_f'].max()) + 1
    td_min = min(df_wx_raw['temp_f'].min(), df_wx_raw['dewpoint_f'].min()) - 1

    data_td = [
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['temp_f'],
                   name='Temperature (F)',
                   line=dict(color='rgb(255, 95, 63)', width=3),
                   xaxis='x', yaxis='y',
                   mode='lines'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['dewpoint_f'],
                   name='Dewpoint (F)',
                   line=dict(color='rgb(255, 127, 63)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
    ]

    layout_td = go.Layout(autosize=True,
                          height=200,
                          yaxis=dict(domain=[0.02, 0.98],
                                     title='Temperature (F)',
                                     range=[td_min, td_max],
                                     fixedrange=True,
                                     titlefont=dict(color='rgb(255, 95, 63)')
                                     ),
                          yaxis2=dict(domain=[0.02, 0.98],
                                      title='Dewpoint (F)',
                                      overlaying='y',
                                      side='right',
                                      range=[td_min, td_max],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(255, 127, 63)')
                                      ),
                          xaxis=dict(type='date',
                                     # fixedrange=True,
                                     range=[dt_min, dt_max],
                                     ),
                          margin=dict(r=50, t=30, b=30, l=60, pad=0),
                          showlegend=False,
                          )

    data_pr = [
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['pressure_in'],
                   name='Pressure (inHg)',
                   line=dict(color='rgb(127, 255, 63)', width=3),
                   xaxis='x', yaxis='y',
                   mode='lines'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['relative_humidity'],
                   name='Humidity (%)',
                   line=dict(color='rgb(63, 127, 255)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
    ]

    layout_pr = go.Layout(autosize=True,
                          height=200,
                          yaxis=dict(domain=[0.02, 0.98],
                                     title='Pressure (inHg)',
                                     # range=[0,120],
                                     fixedrange=True,
                                     titlefont=dict(color='rgb(127, 255, 63)')
                                     ),
                          yaxis2=dict(domain=[0.02, 0.98],
                                      title='Humidity (%)',
                                      overlaying='y',
                                      side='right',
                                      # range=[0,120],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(63, 127, 255)')
                                      ),
                          xaxis=dict(type='date',
                                     # fixedrange=True,
                                     range=[dt_min, dt_max],
                                     ),
                          margin=dict(r=50, t=30, b=30, l=60, pad=0),
                          showlegend=False,
                          )

    data_pc = [
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['precip_1hr_in'],
                   name='Precip (in/hr)',
                   line=dict(color='rgb(31, 190, 255)', width=3),
                   xaxis='x', yaxis='y',
                   mode='lines'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['precip_cum_in'],
                   name='Precip Cumulative (in)',
                   line=dict(color='rgb(63, 255, 255)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
    ]

    layout_pc = go.Layout(autosize=True,
                          height=200,
                          yaxis=dict(domain=[0.02, 0.98],
                                     title='Precip (in/hr)',
                                     # range=[0,120],
                                     fixedrange=True,
                                     titlefont=dict(color='rgb(31, 190, 255)')
                                     ),
                          yaxis2=dict(domain=[0.02, 0.98],
                                      title='Precip Cumulative (in)',
                                      overlaying='y',
                                      side='right',
                                      # range=[0,120],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(63, 255, 255)')
                                      ),
                          xaxis=dict(type='date',
                                     # fixedrange=True,
                                     range=[dt_min, dt_max],
                                     ),
                          margin=dict(r=50, t=30, b=30, l=60, pad=0),
                          showlegend=False,
                          )

    data_wd = [
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['wind_degrees'],
                   name='Wind Direction (degrees)',
                   marker=dict(color='rgb(190, 63, 255)',
                               size=8, symbol='x'),
                   xaxis='x', yaxis='y',
                   mode='markers'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['wind_gust_mph'] * 0.869,
                   name='Wind Gust (kts)',
                   line=dict(color='rgb(31, 190, 15)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['wind_mph'] * 0.869,
                   name='Wind Speed (kts)',
                   line=dict(color='rgb(127, 255, 31)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
    ]

    layout_wd = go.Layout(autosize=True,
                          height=200,
                          yaxis=dict(domain=[0.02, 0.98],
                                     title='Wind Direction (degrees)',
                                     range=[0, 360],
                                     fixedrange=True,
                                     titlefont=dict(color='rgb(190, 63, 255)')
                                     ),
                          yaxis2=dict(domain=[0.02, 0.98],
                                      title='Wind Speed / Gust (kts)',
                                      overlaying='y',
                                      side='right',
                                      # range=[0,120],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(127, 255, 31)')
                                      ),
                          xaxis=dict(type='date',
                                     # fixedrange=True,
                                     range=[dt_min, dt_max],
                                     ),
                          margin=dict(r=50, t=30, b=30, l=60, pad=0),
                          showlegend=False,
                          )

    data_su = [
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['solar_radiation'],
                   name='Solar Radiation (W/m<sup>2</sup>)',
                   line=dict(color='rgb(255, 63, 127)', width=3),
                   xaxis='x', yaxis='y',
                   mode='lines'),
        go.Scatter(x=df_wx_raw.index,
                   y=df_wx_raw['UV'],
                   name='UV',
                   line=dict(color='rgb(255, 190, 63)', width=3),
                   xaxis='x', yaxis='y2',
                   mode='lines'),
    ]

    layout_su = go.Layout(autosize=True,
                          height=200,
                          yaxis=dict(domain=[0.02, 0.98],
                                     title='Solar Radiation (W/m<sup>2</sup>)',
                                     # range=[0,120],
                                     fixedrange=True,
                                     titlefont=dict(color='rgb(255, 63, 127)')
                                     ),
                          yaxis2=dict(domain=[0.02, 0.98],
                                      title='UV',
                                      overlaying='y',
                                      side='right',
                                      # range=[0,120],
                                      fixedrange=True,
                                      titlefont=dict(color='rgb(255, 190, 63)')
                                      ),
                          xaxis=dict(type='date',
                                     # fixedrange=True,
                                     range=[dt_min, dt_max],
                                     ),
                          margin=dict(r=50, t=30, b=30, l=60, pad=0),
                          showlegend=False,
                          )

    t1 = go.Barpolar(r=wind_temp['>10'], theta=wind_temp['wind_cat'],
                     name='>10 mph', width=10,
                     base=0,
                     marker=dict(color='#ffff00', line=dict(color='#ffff00')),
                     )
    t2 = go.Barpolar(r=wind_temp['5-10'], theta=wind_temp['wind_cat'],
                     name='5-10 mph', width=10,
                     base=0,
                     marker=dict(color='#ffcc00', line=dict(color='#ffcc00')),
                     )
    t3 = go.Barpolar(r=wind_temp['2-5'], theta=wind_temp['wind_cat'],
                     name='2-5 mph', width=10,
                     base=0,
                     marker=dict(color='#bfff00', line=dict(color='#bfff00')),
                     )
    t4 = go.Barpolar(r=wind_temp['1-2'], theta=wind_temp['wind_cat'],
                     name='1-2 mph', width=10,
                     base=0,
                     marker=dict(color='#00cc00', line=dict(color='#00cc00')),
                     )
    t5 = go.Barpolar(r=wind_temp['0-1'], theta=wind_temp['wind_cat'],
                     name='0-1 mph', width=10,
                     base=0,
                     marker=dict(color='#009999', line=dict(color='#009999')),
                     )
    t6 = go.Barpolar(r=wind_temp['calm'], theta=wind_temp['wind_cat'],
                     name='calm', width=10,
                     base=0,
                     marker=dict(color='#3366ff', line=dict(color='#3366ff')),
                     )

    data_wr = [t1, t2, t3, t4, t5, t6]

    layout_wr = go.Layout(
        polar=dict(
            radialaxis=dict(
                #visible = False,
                showline=False,
                showticklabels=False,
                ticks='',
                range=[0, wind_temp['>10'].max()],
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
            )
        ),
        #showlegend = False,
        # height=400,
        width=500,
    )

    graphJSON_td = json.dumps(dict(data=data_td, layout=layout_td),
                              cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_pr = json.dumps(dict(data=data_pr, layout=layout_pr),
                              cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_pc = json.dumps(dict(data=data_pc, layout=layout_pc),
                              cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_wd = json.dumps(dict(data=data_wd, layout=layout_wd),
                              cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_su = json.dumps(dict(data=data_su, layout=layout_su),
                              cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON_wr = json.dumps(dict(data=data_wr, layout=layout_wr),
                              cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON_td, graphJSON_pr, graphJSON_pc, graphJSON_wd, graphJSON_su, graphJSON_wr
