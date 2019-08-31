from pymongo import MongoClient
import pandas as pd
import matplotlib
from matplotlib import cm
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
    
def colormap(cs, pl_entries):
    cmap = matplotlib.cm.get_cmap(cs)
    h = 1.0/(pl_entries-1)
    pl_colorscale = []
    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
    return pl_colorscale

def get_sensors(value):
    client=MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.iot
    sensors_all = db.raw.distinct('entity_id')
    sensors = []
    for s in sensors_all:
        sensors.append(s)
        #if value in s:
        #    sensors.append(s)
    return sensors

def get_awc(value):
    values = ['flight_category','temp_c','dewpoint_c','altim_in_hg','wind_dir_degrees',
    'wind_speed_kt','wind_gust_kt','visibility_statute_mi','cloud_base_ft_agl_0',
    'sky_cover_0', 'precip_in', 'elevation_m']

    client = MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.wx
    df_weather_awc = pd.DataFrame(list(db.awc.find()))
    df_weather_awc = df_weather_awc[['latitude','longitude',values[value],'raw_text']]
    return df_weather_awc

def get_aprs(script, limit):
    client = MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.aprs
    if script == 'prefix':
        df_aprs_raw = pd.DataFrame(list(db.raw.find({'script':script,'from':'KK6GPV','latitude':{'$exists':True,'$ne':None}}).sort([('timestamp_', -1)]).limit(limit)))
    else:
        df_aprs_raw = pd.DataFrame(list(db.raw.find({'script':script,'latitude':{'$exists':True,'$ne':None}}).sort([('timestamp_', -1)]).limit(limit)))
    df_aprs_raw = df_aprs_raw[['timestamp_','latitude','longitude','script','altitude','speed','course','raw']]
    return df_aprs_raw

def get_iot(value, device):
    client=MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.iot
    df_iot = pd.DataFrame(list(db.raw.find({'entity_id':device}).sort([('_id', -1)]).limit(value)))
    return df_iot

def get_vib(value):
    client=MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.iot
    df_vib = pd.DataFrame(list(db.vib.find().sort([('_id', -1)]).limit(value)))
    return df_vib

def get_wx(sid, value):
    client=MongoClient('mongodb+srv://web:web@cluster0-li5mj.gcp.mongodb.net')
    db = client.wx
    df_wx_raw = pd.DataFrame(list(db.raw.find({'station_id':sid}).sort([('observation_time_rfc822', -1)]).limit(value)))
    df_wx_raw.index = df_wx_raw['observation_time_rfc822']
    #df_wx_raw = df_wx_raw.tz_localize('UTC').tz_convert('US/Central')

    for col in df_wx_raw.columns:
        try:
            df_wx_raw.loc[df_wx_raw[col] < -50, col] = pd.np.nan
        except:
            pass

    df_wx_raw['cloudbase'] = ((df_wx_raw['temp_f'] - df_wx_raw['dewpoint_f']) / 4.4) * 1000 + 50
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
    df_wx_raw.loc[df_wx_raw['precip_today_delta'] < 0, 'precip_today_delta'] = 0
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

    df_wx_raw['wind_degrees_cat'] = np.floor(df_wx_raw['wind_degrees'] / 15) * 15
    df_wx_raw.loc[df_wx_raw['wind_degrees_cat'] == 360, 'wind_degrees_cat'] = 0
    df_wx_raw['wind_degrees_cat'] = df_wx_raw['wind_degrees_cat'].astype(int).astype(str)
    
    df_wx_raw.loc[df_wx_raw['wind_mph'] == 0, 'wind_degrees'] = pd.np.nan

    wind = df_wx_raw[['wind_cat','wind_degrees_cat']]
    wind['count'] = 1
    ct = len(wind)
    wind = pd.pivot_table(wind, values='count', index=['wind_degrees_cat'], columns=['wind_cat'], aggfunc=np.sum)
    ix=np.arange(0,360,5)
    col=['calm','0-1','1-2','2-5','5-10','>10']
    wind_temp = pd.DataFrame(data=0, index=ix,columns=col)
    for i in ix:
        for j in col:
            try:
                wind_temp.loc[i,j] = wind.loc[str(i),j]
            except:
                pass
    wind_temp = wind_temp.fillna(0)
    wind_temp['calm'] = wind_temp['calm'].mean()
    for col in range(len(wind_temp.columns)):
        try:
            wind_temp.iloc[:,col] = wind_temp.iloc[:,col] + wind_temp.iloc[:,col-1]
        except:
            pass
    wind_temp = np.round(wind_temp / ct * 100, 2)
    wind_temp['wind_cat'] = wind_temp.index
    return df_wx_raw, wind_temp
