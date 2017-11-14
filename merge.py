#!/usr/bin/env python3
'''
Combine the station locations and forecast JSON documents into a single
document.
'''

import json
import pandas as pd


with open('data/forecast.json') as f:
    forecast = json.load(f)

with open('data/stations.json') as f:
    stations = json.load(f)

for location in stations:
    code = location.pop('code')
    forecast[code]['forecast-name'] = forecast[code].pop('name')
    forecast[code].update(location)

with open('data/merged.json', 'w') as f:
    json.dump(forecast, f)
