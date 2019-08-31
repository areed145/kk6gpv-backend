import plotly.graph_objs as go

values = ['flight_category','temp_c','dewpoint_c','altim_in_hg','wind_dir_degrees',
    'wind_speed_kt','wind_gust_kt','visibility_statute_mi','cloud_base_ft_agl_0',
    'sky_cover_0', 'precip_in', 'elevation_m']
units = ['','C','C','inHg','degrees',
        'kts','kts','sm','ft AGL',
        'degrees','degrees','m']
names = ['Flight Category','Temperature (C)','Dewpoint (C)','Altimeter (inHg)','Wind Direction (degrees)',
        'Wind Speed (kts)','Wind Gust (kts)','Visibility (sm)','Cloud Base (ft AGL)',
        'Sky Cover','Precip (in)','Elevation (m)']
mins = [0,-10,-10,29.5,0,
        0,0,0,0,
        0,0,0]
maxs = [0,30,30,30.5,359,
        30,30,10,2000,
        0,4,2000]

def dropdown_awc():
    return [{'label': names[i], 'value': i} for i in range(len(values))]

def fig_awc(df_weather_awc, value):
    mapbox_access_token = 'pk.eyJ1IjoiYXJlZWQxNDUiLCJhIjoiY2phdzNsN2ZoMGh0bjMybzF3cTkycWYyciJ9.4aS7z-guI2VDlP3duMg2FA'

    cs = [
        [0.0,'#424ded'],
        [0.1,'#4283ed'],
        [0.2,'#42d0ed'],
        [0.3,'#42edae'],
        [0.4,'#78ed42'],
        [0.5,'#d6ed42'],
        [0.6,'#edde42'],
        [0.7,'#f4af41'],
        [0.8,'#f48541'],
        [0.9,'#f44741'],
        [1.0,'#f44298']
        ]

    if value in [6,7]:
        cs = [
        [0.0,'#f44741'],
        [0.2,'#f48541'],
        [0.4,'#f4af41'],
        [0.6,'#edde42'],
        [0.8,'#d6ed42'],
        [1.0,'#78ed42']
        ]

    if value == 0:
        df_vfr = df_weather_awc[df_weather_awc['flight_category'] == 'VFR']
        df_mvfr = df_weather_awc[df_weather_awc['flight_category'] == 'MVFR']
        df_ifr = df_weather_awc[df_weather_awc['flight_category'] == 'IFR']
        df_lifr = df_weather_awc[df_weather_awc['flight_category'] == 'LIFR']

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
    elif value == 9:
        df_clr = df_weather_awc[df_weather_awc['sky_cover_0'] == 'CLR']
        df_few = df_weather_awc[df_weather_awc['sky_cover_0'] == 'FEW']
        df_sct = df_weather_awc[df_weather_awc['sky_cover_0'] == 'SCT']
        df_bkn = df_weather_awc[df_weather_awc['sky_cover_0'] == 'BKN']
        df_ovc = df_weather_awc[df_weather_awc['sky_cover_0'] == 'OVC']
        df_ovx = df_weather_awc[df_weather_awc['sky_cover_0'] == 'OVX']

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
        data = [go.Scattermapbox(lat=df_weather_awc['latitude'], 
                                lon=df_weather_awc['longitude'], 
                                text=df_weather_awc['raw_text'],
                                mode='markers', 
                                marker=dict(size=10,
                                            color=df_weather_awc[values[value]],
                                            colorbar=dict(title=units[value]),
                                            colorscale=cs,
                                            cmin=mins[value],
                                            cmax=maxs[value],
                                            )
                                )
        ]

    layout = go.Layout(autosize=True,
                        #height=1000,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(r=0, t=0, b=0, l=0, pad=0), 
                        mapbox=dict(bearing=0,
                                    center=dict(lat=38, lon=-96),
                                    accesstoken=mapbox_access_token,
                                    style='satellite-streets',
                                    pitch=0, 
                                    zoom=3
                                    )
                        )

    fig = dict(data=data, layout=layout)
    return fig