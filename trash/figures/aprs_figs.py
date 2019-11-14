import plotly.graph_objs as go

values = ['script','altitude','speed','course']
units = ['','ft','mph','degrees']
names = ['None','Altitude','Speed (mph)','Course (degrees)']
mins = [0,0,0,0]
maxs = [0,1000,100,359]
mult = [0,3.2808,0.621371,1]

def dropdown_aprs():
    return [{'label': names[i], 'value': i} for i in range(len(values))]

def fig_aprs(df_aprs_raw, value):
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

    if value == 0:
        data_map = [go.Scattermapbox(lat=df_aprs_raw['latitude'], 
                                lon=df_aprs_raw['longitude'], 
                                text=df_aprs_raw['raw'],
                                mode='markers', 
                                marker=dict(size=10)
                                )
        ]
    else:
        data_map = [go.Scattermapbox(lat=df_aprs_raw['latitude'], 
                                lon=df_aprs_raw['longitude'], 
                                text=df_aprs_raw['raw'],
                                mode='markers', 
                                marker=dict(size=10,
                                            color=mult[value] * df_aprs_raw[values[value]],
                                            colorbar=dict(title=units[value]),
                                            colorscale=cs,
                                            cmin=mins[value],
                                            cmax=maxs[value],
                                            )
                                )
        ]

    layout_map = go.Layout(autosize=True,
                        #height=1000,
                        showlegend=False,
                        hovermode='closest',
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
        go.Scatter(x=df_aprs_raw['timestamp_'],
            y=df_aprs_raw['speed'],
            name='Speed (mph)',
            line=dict(color='rgb(255, 127, 63)', width=2, shape='linear'),
            #xaxis='x', yaxis='y',
            mode='lines'),
    ]

    layout_speed = go.Layout(autosize=True,
        height=200,
        yaxis=dict(domain=[0.02, 0.98],
            title='Speed (mph)',
            #range=[td_min,td_max],
            fixedrange=True,
            titlefont=dict(color='rgb(255, 95, 63)')
        ),
        xaxis=dict(type='date', fixedrange=False),
        margin=dict(r=50, t=30, b=30, l=60, pad=0),
        showlegend=False,
    )

    data_alt = [
        go.Scatter(x=df_aprs_raw['timestamp_'],
            y=df_aprs_raw['altitude'],
            name='Altitude (ft)',
            line=dict(color='rgb(255, 95, 63)', width=2, shape='linear'),
            #xaxis='x', yaxis='y',
            mode='lines'),
    ]

    layout_alt = go.Layout(autosize=True,
        height=200,
        yaxis=dict(domain=[0.02, 0.98],
            title='Altitude (ft)',
            #range=[td_min,td_max],
            fixedrange=True,
            titlefont=dict(color='rgb(255, 95, 63)')
        ),
        xaxis=dict(type='date', fixedrange=False),
        margin=dict(r=50, t=30, b=30, l=60, pad=0),
        showlegend=False,
    )

    data_course = [
        go.Scatter(x=df_aprs_raw['timestamp_'],
            y=df_aprs_raw['course'],
            name='Course (degrees)',
            line=dict(color='rgb(255, 63, 63)', width=2, shape='linear'),
            #xaxis='x', yaxis='y',
            mode='lines'),
    ]

    layout_course = go.Layout(autosize=True,
        height=200,
        yaxis=dict(domain=[0.02, 0.98],
            title='Course (degrees)',
            #range=[td_min,td_max],
            fixedrange=True,
            titlefont=dict(color='rgb(255, 95, 63)')
        ),
        xaxis=dict(type='date', fixedrange=False),
        margin=dict(r=50, t=30, b=30, l=60, pad=0),
        showlegend=False,
    )

    map_aprs = dict(data=data_map, layout=layout_map)
    graph_speed = dict(data=data_speed, layout=layout_speed)
    graph_alt = dict(data=data_alt, layout=layout_alt)
    graph_course = dict(data=data_course, layout=layout_course)

    return map_aprs, graph_speed, graph_alt, graph_course