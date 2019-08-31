import flask
import dns
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from helpers import data_helpers, image_helpers
from figures import awc_figs, iot_figs, wx_figs, aprs_figs

# from apscheduler.schedulers.background import BackgroundScheduler
# sched = BackgroundScheduler(daemon=True)
# sched.add_job(fetchers.,'interval',minutes=60)
# sched.start()

server = flask.Flask(__name__)

navbar = dbc.Navbar(
    dbc.Nav(
        children=[
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(image_helpers.get_image('icon_transparent.png')), height='40px')),
                        dbc.Col(dbc.NavbarBrand('Coconut Barometer', className='ml-2')),
                    ],
                    align='center',
                    no_gutters=True,
                ),
                href="http://159.89.146.242/#",
            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Weather",
                children=[
                    dbc.DropdownMenuItem('Aviation Weather', href='http://159.89.146.242/awc'),
                    dbc.DropdownMenuItem('Station Weather', href='http://159.89.146.242/wx'),
                    #dbc.DropdownMenuItem(divider=True),
                ],
            ),
            dbc.NavItem(dbc.NavLink('IOT', href='http://159.89.146.242/iot')),
            dbc.NavItem(dbc.NavLink('APRS', href='http://159.89.146.242/aprs')),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Flying",
                children=[
                    dbc.DropdownMenuItem('Aircraft', href='http://159.89.146.242/aircraft'),
                    dbc.DropdownMenuItem('Paragliding', href='http://159.89.146.242/paragliding'),
                    dbc.DropdownMenuItem('Soaring', href='http://159.89.146.242/soaring'),
                    dbc.DropdownMenuItem('N5777V', href='http://159.89.146.242/n5777v'),
                ],
            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Photos",
                children=[
                    dbc.DropdownMenuItem('Galleries', href='http://159.89.146.242/galleries'),
                    dbc.DropdownMenuItem('Travel', href='http://159.89.146.242/travel'),
                    dbc.DropdownMenuItem('Scuba', href='http://159.89.146.242/scuba'),
                    dbc.DropdownMenuItem('Fishing', href='http://159.89.146.242/fishing'),
                ],
            ),
            dbc.NavItem(dbc.NavLink('Oil & Gas', href='http://159.89.146.242/oilgas')),       
        ],
    ),
sticky='top',
color='rgb(200, 255, 255)',
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Heading"),
                        html.P(
                            """\
Donec id elit non mi porta gravida at eget metus.
Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum
nibh, ut fermentum massa justo sit amet risus. Etiam porta sem
malesuada magna mollis euismod. Donec sed odio dui. Donec id elit non
mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus
commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit
amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed
odio dui."""
                        ),
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)

app = dash.Dash(
    __name__,
    server=server,
    #routes_pathname_prefix='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([navbar])

awc_page = html.Div(children=[
    navbar,

    html.H1(children='Aviation Weather'),

    dcc.Dropdown(
        id='dropdown',
        options=awc_figs.dropdown_awc(),
        value=0
    ),

    dcc.Graph(id='map_awc', 
        config={'displayModeBar': False},
        style={'width': '100vw', 'height': '70vh'},
    ),
])

@app.callback(
    Output('map_awc','figure'),
    [Input('dropdown','value')])
def update_awc(value):
    df_weather_awc = data_helpers.get_awc(value)
    return awc_figs.fig_awc(df_weather_awc, value)  

iot_page = html.Div(children=[
    navbar,

    html.H1(children='IOT'),

    dcc.Dropdown(
        id='dropdown_device',
        options=[{'label': i, 'value': i} for i in data_helpers.get_sensors('')],
        value='temperature'
    ),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [100,500,1000,5000,10000,25000,100000]],
        value=100
    ),

    dcc.Graph(id='fig_temp_hum', config={'displayModeBar': False}),

    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(
    Output('fig_temp_hum','figure'),
    [Input('dropdown','value'),Input('dropdown_device','value'),Input('interval-component','n_intervals')])
def update_iot(value,device,n):
    dfs = []
    dfs.append(data_helpers.get_iot(value, device))
    #for sensor in data_helpers.get_sensors(device):
    #    dfs.append(data_helpers.get_iot(value, sensor))
    return iot_figs.fig_iot(dfs)

vib_page = html.Div(children=[
    navbar,

    html.H1(children='Vibration Analysis'),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [10,25,50,100,250]],
        value=100
    ),

    dcc.Graph(id='vib_hm', config={'displayModeBar': False}),

    dcc.Graph(id='vib_fft', config={'displayModeBar': False}),

    dcc.Graph(id='vib_qc', config={'displayModeBar': False}),

    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(
    [Output('vib_hm','figure'),Output('vib_fft','figure'),Output('vib_qc','figure')],
    [Input('dropdown','value'),Input('interval-component','n_intervals')])
def update_vib(value, n):
    df_iot_vib = data_helpers.get_vib(value)
    vib_hm, vib_fft, vib_qc = iot_figs.figs_vib(df_iot_vib)
    return vib_hm, vib_fft, vib_qc

wx_page = html.Div(children=[
    navbar,

    html.H1(children='Station Weather'),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [100,500,1000,5000,10000,25000,100000]],
        value=100
    ),

    dcc.Graph(id='fig_td', config={'displayModeBar': False}),

    dcc.Graph(id='fig_pr', config={'displayModeBar': False}),

    dcc.Graph(id='fig_pc', config={'displayModeBar': False}),

    dcc.Graph(id='fig_wd', config={'displayModeBar': False}),

    dcc.Graph(id='fig_su', config={'displayModeBar': False}),

    dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(
    [Output('fig_td','figure'),Output('fig_pr','figure'),Output('fig_pc','figure'),Output('fig_wd','figure'),Output('fig_su','figure')],
    [Input('dropdown','value'),Input('interval-component','n_intervals')])
def update_wx(value,n):
    df_wx_raw, wind_temp = data_helpers.get_wx('KTXHOUST1930', value)
    fig_td, fig_pr, fig_pc, fig_wd, fig_su = wx_figs.figs_wx(df_wx_raw, wind_temp)
    return fig_td, fig_pr, fig_pc, fig_wd, fig_su

aprs_page = html.Div(children=[
    navbar,

    html.H1(children='APRS'),

    dcc.Dropdown(
        id='dropdown_script',
        options=[{'label': i, 'value': i} for i in ['prefix','entry','radius']],
        value='prefix'
    ),

    dcc.Dropdown(
        id='dropdown_prop',
        options=aprs_figs.dropdown_aprs(),
        value=1
    ),

    dcc.Dropdown(
        id='dropdown_limit',
        options=[{'label': i, 'value': i} for i in [100,500,1000,5000,10000,25000,100000]],
        value=100
    ),

    dcc.Graph(id='map_aprs', 
        config={'displayModeBar': False},
        style={'width': '100vw', 'height': '60vh'},
    ),

    dcc.Graph(id='graph_speed', 
        config={'displayModeBar': False},
        style={'width': '100vw', 'height': '200'},
    ),

    dcc.Graph(id='graph_alt', 
        config={'displayModeBar': False},
        style={'width': '100vw', 'height': '200'},
    ),

    dcc.Graph(id='graph_course', 
        config={'displayModeBar': False},
        style={'width': '100vw', 'height': '200'},
    ),

    dash_table.DataTable(id='table_aprs',
        columns=[{"name": i, "id": i} for i in ['timestamp','latitude','longitude','altitude','speed','course','raw']],
        style_header={
            'backgroundColor': '#C8FFFF',
            'fontWeight': 'bold',
            'textAlign': 'center',
        }
        #data=[],
        #filterable=True,
        #sortable=True,
    ),
])

@app.callback(
    [Output('map_aprs','figure'),Output('graph_speed','figure'),Output('graph_alt','figure'),Output('graph_course','figure'),Output('table_aprs','data')],
    [Input('dropdown_prop','value'),Input('dropdown_script','value'),Input('dropdown_limit','value')])
def update_aprs(prop, script, limit):
    df_aprs_raw = data_helpers.get_aprs(script, limit)
    map_aprs, graph_speed, graph_alt, graph_course = aprs_figs.fig_aprs(df_aprs_raw, prop)
    df_aprs_raw['latitude'] = np.round(df_aprs_raw['latitude'],4)
    df_aprs_raw['longitude'] = np.round(df_aprs_raw['longitude'],4)
    df_aprs_raw['altitude'] = np.round(df_aprs_raw['altitude'],4)
    df_aprs_raw['speed'] = np.round(df_aprs_raw['speed'],2)
    df_aprs_raw['timestamp'] = df_aprs_raw['timestamp_'].astype('datetime64[s]')
    #df_aprs_raw.rename({'timestamp_': 'timestamp'}, axis=1, inplace=True)
    df_aprs_raw = df_aprs_raw.to_dict('rows')
    return map_aprs, graph_speed, graph_alt, graph_course, df_aprs_raw

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/aprs':
        return aprs_page
    elif pathname == '/awc':
        return awc_page
    elif pathname == '/iot':
        return iot_page
    elif pathname == '/vib':
        return vib_page
    elif pathname == '/wx':
        return wx_page
    elif pathname == '/test':
        return flask.render_template('404.html', title='test')
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)