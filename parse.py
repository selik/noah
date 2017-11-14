#!/usr/bin/env python3
'''

Parse station locations and forecasts from HTML-format, saving in JSON-
format. The station locations are in columnar text in pre-formatted tags
inside the HTML document.

```
STN         NAME          ST     LAT      LON   
PHHI WHEELER AAF          HI   21.48N   158.03W
PHJH LAHAINA/WEST MAUI    HI   21.02N   156.63W
PHJR KALAELOA ARPT/OAHU   HI   21.32N   158.07W
PHKO KONA/KEAHOLE         HI   19.65N   156.00W
PHLI LIHUE                HI   21.98N   159.35W
```

Each station reports its current observations and a 24-hour forecast
every hour. These observations and forecasts are also written in
columnar text inside "pre" tags.

```
PHHI   WHEELER AAF           GFS LAMP GUIDANCE  11/06/2017  2300 UTC            
 UTC  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 
 TMP  81 80 79 78 76 75 74999999999999999999999999999999999 71 75 77 79 79 80 79 
 DPT  65 65 65 65 66 66 66999999999999999999999999999999999 66 67 66 65 65 65 65 
 WDR  09 09 08 08 07 08 14 99 99 99 99 99 99 99 99 99 99 99 24 12 09 09 09 08 08 
 WSP  09 09 08 10 06 04 02 99 99 99 99 99 99 99 99 99 99 99 01 03 06 07 08 09 09 
 WGS  NG NG NG NG NG NG NG999999999999999999999999999999999 NG NG NG NG NG NG NG 
 PPO   1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  2  1  0  2 
 PCO   N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N 
 P06                     0                 9                 6                12 
 CLD  BK BK SC FW FW FW FW FW FW FW CL CL CL CL CL CL CL CL CL FW FW SC BK BK BK 
 CIG   6  6  6  6  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  7  6  6  6 
 CCG   6  6  6  6  6  6  6  6  6  6  6  3  4  5  6  6  6  6  6  6  6  6  6  5  5 
 VIS   7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7 
 CVS   7  7  7  7  7  7  7  7  7  7  7  7  7  6  7  6  7  6  7  7  7  6  7  7  6 
 OBV   N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N 
```

'''

import json
import re


### Locations ##########################################################

station_re = re.compile(' +'.join([r'([A-Z0-9]{4}) (.*?)',
                                   r'([A-Z]{2})',
                                   r'([0-9.\-]+[NS])',
                                   r'([0-9.\-]+[EW])']))

stations = []
with open('data/stations.html') as f:
    for line in f:
        mo = station_re.search(line)
        if mo is not None:
            code, name, state, lat, lng = mo.groups()
            row = {'code': code,
                   'name': name,
                   'state': state,
                   'latitude': lat,
                   'longitude': lng}
            stations.append(row)
            
with open('data/stations.json', 'w') as f:
    json.dump(stations, f, indent=2)


### Forecast ###########################################################

header_re = re.compile(' +'.join([r'([A-Z0-9]{4})',
                                  r'(.*?)',
                                  r'GFS LAMP GUIDANCE',
                                  r'([0-9/ ]+ UTC)']))

metric_re = re.compile(r'([A-Z0-9]{3}) ' + r'([A-Z0-9 \-]{3})' * 25)

forecast = {}
with open('data/forecast.html') as f:
    for line in f:
        mo = header_re.search(line)
        if mo is not None:
            code, name, timestring = mo.groups()
            forecast[code] = {'name': name, 'time': timestring, 'data': {}}
        mo = metric_re.search(line)
        if mo is not None:
            metric, *values = mo.groups()
            values = [s.strip() for s in values]
            try:
                values = [int(s) for s in values]
            except ValueError:
                pass
            forecast[code]['data'][metric] = values
            
with open('data/forecast.json', 'w') as f:
    json.dump(forecast, f, indent=2)
