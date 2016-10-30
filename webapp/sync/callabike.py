# encoding: utf-8

"""
Copyright (c) 2012 - 2016, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ..models import *
from webapp import db
import requests
import datetime
from HTMLParser import HTMLParser
from lxml import etree
import time

def sync():
  print "Import Call a Bike"
  base_url = 'https://www.callabike-interaktiv.de/kundenbuchung/hal2ajax_process.php'
  
  url_post_params_city = {
    'after': '',
    'ajxmod': 'hal2map',
    'hal2map': '',
    'bereich': '',
    'before': '',
    'callee': 'getMarker',
    'getMarker': '',
    'centerLat': 51.46736714249796,
    'centerLng': 7.221625510099341,
    'key': '',
    'lat1': 47.27,
    'lat2': 55.05,
    'lng1': 5.87,
    'lng2': 15.03,
    'mapstadt_id': '',
    'mapstation_id': '',
    'requester': 'bikesuche',
    'buchanfrage_erg': '',
    'searchmode': 'default',
    'default': '',
    'stadtCache': '',
    'staedtelist': '',
    'verwaltungfirma': '',
    'webfirma_id': '',
    'with_staedte': 'J',
    'zoom': '13'
  }
  
  r = requests.post(base_url, params=url_post_params_city, verify=False)
  html_parser = HTMLParser()
  
  raw_city_data = r.json()
  sharing_provider = SharingProvider.query.filter_by(slug='callabike')
  if sharing_provider.count():
    sharing_provider = sharing_provider.first()
  else:
    sharing_provider = SharingProvider()
    sharing_provider.created = datetime.datetime.now()
    sharing_provider.slug = 'callabike'
    sharing_provider.active = 1
  
  sharing_provider.updated = datetime.datetime.now()
  sharing_provider.name = 'Call a Bike'
  db.session.add(sharing_provider)
  db.session.commit()
  
  for raw_city in raw_city_data['marker']:
    time.sleep(0.5)
    url_post_params_station = {
      'after': '',
      'ajxmod': 'hal2map',
      'hal2map': '',
      'bereich': '',
      'before': '',
      'callee': 'getMarker',
      'getMarker': '',
      'centerLat': 51.46736714249796,
      'centerLng': 7.221625510099341,
      'key': '',
      'lat1': 47.27,
      'lat2': 55.05,
      'lng1': 5.87,
      'lng2': 15.03,
      'mapstadt_id': int(raw_city['hal2option']['id'][1:]),
      'mapstation_id': '',
      'requester': 'bikesuche',
      'buchanfrage_erg': '',
      'searchmode': 'default',
      'default': '',
      'stadtCache': '',
      'staedtelist': '',
      'verwaltungfirma': '',
      'webfirma_id': '',
      'with_staedte': 'N',
      'zoom': '13'
    }
  
    r = requests.post(base_url, params=url_post_params_station)
    raw_station_data = r.json()
    for raw_sharing_station in raw_station_data['marker']:
      sharing_station = SharingStation.query.filter_by(external_id=raw_sharing_station['hal2option']['id']).filter_by(sharing_provider_id=sharing_provider.id)
      if sharing_station.count():
        sharing_station = sharing_station.first()
      else:
        sharing_station = SharingStation()
        sharing_station.created = datetime.datetime.now()
        sharing_station.external_id = raw_sharing_station['hal2option']['id']
      if 'tooltip' not in raw_sharing_station['hal2option'] or 'objecttyp' not in raw_sharing_station['hal2option']:
        print raw_sharing_station
      else:
        sharing_station.updated = datetime.datetime.now()
        sharing_station.lat = raw_sharing_station['lat']
        sharing_station.lon = raw_sharing_station['lng']
        sharing_station.name = html_parser.unescape(raw_sharing_station['hal2option']['tooltip']).replace("'", '')
        sharing_station.vehicle_all = len(raw_sharing_station['hal2option']['bikelist'])
        sharing_station.station_type = 1
        sharing_station.sharing_provider_id = sharing_provider.id
        db.session.add(sharing_station)
        db.session.commit()