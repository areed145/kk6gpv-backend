from __future__ import print_function

import flickr_api as f

f.set_keys(api_key='77a2ae7ea816558f00e4dd32249be54e',
           api_secret='2267640a7461db21')
#f.set_auth_handler('helpers/auth')
f.set_auth_handler('auth')

username = '- Adam Reeder -'
u = f.Person.findByUserName(username)
ps = u.getPhotosets()

rows = []
gals = []
idx = 0
for p in ps:
    if idx < 4:
        title = p.title
        pid = p.id
        photos = p.count_photos
        views = p.count_views
        primary = 'https://live.staticflickr.com/8203/'+p.primary+'_'+p.secret+'_q_d.jpg'
        link = 'https://www.flickr.com/photos/adamreeder/albums/'+p.id
        gals.append({'title':title, 'id':pid, 'photos':photos, 'views':views, 'primary':primary, 'link':link})
        idx += 1
    else:
        rows.append(gals)
        gals = []
        idx = 0