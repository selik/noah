#!/usr/bin/env python3
'''
Fetch weather station locations and forecasts as HTML from NOAA GFS LAMP
'''

from urllib.request import urlopen

base_url = 'http://www.nws.noaa.gov/mdl/gfslamp/'
stations_url = base_url + 'docs/stations_info_01142015.shtml'
forecast_url = base_url + 'lavlamp.shtml'

with urlopen(stations_url) as response:
    data = response.read()
html = data.decode()
with open('data/stations.html', 'w') as f:
    f.write(html)

with urlopen(forecast_url) as response:
    data = response.read()
html = data.decode()
with open('data/forecast.html', 'w') as f:
    f.write(html)
