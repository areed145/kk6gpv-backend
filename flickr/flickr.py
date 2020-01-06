#from __future__ import print_function

import flickr_api as f
import pickle
import os
from pymongo import MongoClient
from datetime import datetime
import time

f.set_keys(api_key='77a2ae7ea816558f00e4dd32249be54e',
           api_secret='2267640a7461db21')
f.set_auth_handler('auth')
username = '- Adam Reeder -'
u = f.Person.findByUserName(username)


def get_gals():
    ps = u.getPhotosets()

    gals = {}
    for p in ps:
        pid = p.id
        title = p.title
        count_photos = p.count_photos
        count_views = p.count_views
        primary = 'https://live.staticflickr.com/' + \
            p.server+'/'+p.primary+'_'+p.secret+'_q_d.jpg'
        flickr_link = 'https://www.flickr.com/photos/adamreeder/albums/'+p.id
        kk6gpv_link = '/galleries/'+p.id
        photos = {}
        phs = p.getPhotos()
        for ph in phs:
            photos[ph.id] = {
                'thumb': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_q_d.jpg',
                'large': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_b.jpg'
            }
        gals[pid] = {
            'id': pid,
            'title': title,
            'count_photos': count_photos,
            'count_views': count_views,
            'primary': primary,
            'flickr_link': flickr_link,
            'kk6gpv_link': kk6gpv_link,
            'photos': photos
        }

    # g = open('static/gals', 'wb')
    # pickle.dump(gals, g)
    print('galleries updated')
    db.gals.insert_one(gals)
    return gals

client = MongoClient('mongodb+srv://kk6gpv:kk6gpv@cluster0-kglzh.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client.flickr

if __name__ == '__main__':
    last_hour = datetime.now().hour - 1
    while True:
        if datetime.now().hour != last_hour:
            get_gals()
            last_hour = datetime.now().hour
            print('got long')
        else:
            print('skipping updates')
        time.sleep(60)


