import flickr_api as f

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
    primary = 'https://live.staticflickr.com/8203/'+p.primary+'_'+p.secret+'_q_d.jpg'
    flickr_link = 'https://www.flickr.com/photos/adamreeder/albums/'+p.id
    kk6gpv_link = '/galleries/'+p.id
    photos = {}
    phs = p.getPhotos()
    for ph in phs:
        photos[ph.id] = {
            'thumb': 'https://live.staticflickr.com/8203/'+ph.id+'_'+ph.secret+'_q_d.jpg'}
    gals[pid] = {'id': pid,
                 'title': title,
                 'count_photos': count_photos,
                 'count_views': count_views,
                 'primary': primary,
                 'flickr_link': flickr_link,
                 'kk6gpv_link': kk6gpv_link,
                 'photos': photos
                 }

rows = []
frames = []
idx = 0
for gal in gals:
    if idx < 6:
        frames.append({'caption': gals[gal]['title'] + ' - ' + str(gals[gal]['count_photos']),
                        'thumb': gals[gal]['primary'],
                        'kk6gpv_link': gals[gal]['kk6gpv_link']})
        idx += 1
    else:
        rows.append(frames)
        frames = []
        idx = 0

id =  '72157662536016499'

rows2 = []
frames2 = []
idx = 0
for ph in gals[id]['photos']:
    if idx < 6:
        frames2.append({'thumb': gals[id]['photos'][ph]['thumb'],
                        'kk6gpv_link': '/galleries/'+id+'/'+ph})
        idx += 1
    else:
        rows2.append(frames2)
        frames2 = []
        idx = 0

