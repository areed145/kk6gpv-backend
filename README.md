# kk6gpv-flask
goal will be to re-create kk6gpv.net as a flask site

[![CircleCI](https://circleci.com/gh/areed145/kk6gpv-flask.svg?style=svg)](https://circleci.com/gh/areed145/kk6gpv-flask)

## stack
- python
- mongodb
- flask
- boostrap
- plotly
- leaflet (folium?)
- datashader
- mqtt

## structure
- weather
    - station
    - aviation
- iot
    - home assistant
    - vibration protocol
- aprs
    - prefix
    - entry
    - radius
- flying
    - aircraft
    - paragliding
    - sailplane
    - n5777v
- photos
    - travel
    - flickr gallery
- oil & gas
     - doggr application

## todo
- incorporate fetchers
- UI
- rebuild flickr photo gallery functionality
- add station weather plots
- move gallery listing to db
- incorporate Plotly.react in other plots
- port DOGGR data
- figure out how to add raster layers to maps (leaflet? instaead of plotly for mapbox)
- builder like blog for writing about proejcts
- details pages for APRS info
- styling
- convert time queries to date range

## done
- connect to mongodb
- live updating plots
- rebuild flickr gallery functionality
- add weather maps
- multi-services in kubernetes?
