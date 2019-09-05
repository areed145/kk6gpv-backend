#from __future__ import print_function

import flickr_api as f


def get_gals():
    f.set_keys(api_key='77a2ae7ea816558f00e4dd32249be54e',
               api_secret='2267640a7461db21')
    f.set_auth_handler('helpers/auth')
    username = '- Adam Reeder -'
    u = f.Person.findByUserName(username)
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
                'large': 'https://live.staticflickr.com/'+ph.server+'/'+ph.id+'_'+ph.secret+'_h.jpg'
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
    return gals
