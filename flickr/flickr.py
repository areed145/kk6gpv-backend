#from __future__ import print_function

import flickr_api as f
import pickle
import os
from pymongo import MongoClient
from datetime import datetime
import time
import numpy as np
f.set_keys(api_key='77a2ae7ea816558f00e4dd32249be54e',
           api_secret='2267640a7461db21')
# f.set_auth_handler('auth')
username = '- Adam Reeder -'
u = f.Person.findByUserName(username)


def get_gals():
    ps = u.getPhotosets()

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

        for page in range(int(np.ceil(p.photos/500))):
            phs = p.getPhotos(page=page)

            for ph in phs:

                photo = {
                    'id': ph.id,
                    'thumb': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_q_d.jpg',
                    'large': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_b.jpg',
                }
                try:
                    ex = {}
                    for item in ph.getExif():
                        ex[item.tag] = item.raw
                    photo['exif'] = ex
                except:
                    pass
                try:
                    photo['location'] = ph.location
                except:
                    pass
                db.photos.replace_one({'id': ph.id}, photo, upsert=True)
                print('photo uploaded')

                photos[ph.id] = {
                    'thumb': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_q_d.jpg',
                    'large': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_b.jpg',
                }
                try:
                    photos[ph.id]['latitude'] = ph.location['latitude']
                    photos[ph.id]['longitude'] = ph.location['longitude']
                except:
                    pass

        gal = {
            'id': pid,
            'title': title,
            'count_photos': count_photos,
            'count_views': count_views,
            'primary': primary,
            'flickr_link': flickr_link,
            'kk6gpv_link': kk6gpv_link,
            'photos': photos
        }
        db.galleries.replace_one({'id': pid}, gal, upsert=True)
        print('gallery updated')


client = MongoClient(os.environ['MONGODB_CLIENT'])
db = client.flickr

if __name__ == '__main__':
    last_day = datetime.now().day - 1
    while True:
        if datetime.now().day != last_day:
            get_gals()
            last_day = datetime.now().day
            print('got long')
        else:
            print('skipping updates')
        time.sleep(60)
