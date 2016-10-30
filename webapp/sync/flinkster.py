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
from lxml import etree

def sync():
  print "Import Flinkster"
  base_url = 'https://www.flinkster.de/kundenbuchung/hal2ajax_process.php'
  
  url_post_params = {
    'after': '',
    'ajxmod': 'hal2map',
    'hal2map': '',
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
    'requester': 'stadtmap',
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
  
  r = requests.post(base_url, params=url_post_params, verify=False)
  
  raw_data = r.json()
  sharing_provider = SharingProvider.query.filter_by(slug='flinkster')
  if sharing_provider.count():
    sharing_provider = sharing_provider.first()
  else:
    sharing_provider = SharingProvider()
    sharing_provider.created = datetime.datetime.now()
    sharing_provider.slug = 'flinkster'
    sharing_provider.active = 1
  
  sharing_provider.updated = datetime.datetime.now()
  sharing_provider.name = 'Flinkster'
  db.session.add(sharing_provider)
  db.session.commit()
  
  for raw_sharing_station in raw_data['marker']:
    sharing_station = SharingStation.query.filter_by(external_id=raw_sharing_station['hal2option']['id']).filter_by(sharing_provider_id=sharing_provider.id)
    if sharing_station.count():
      sharing_station = sharing_station.first()
    else:
      sharing_station = SharingStation()
      sharing_station.created = datetime.datetime.now()
      sharing_station.external_id = raw_sharing_station['hal2option']['id']
    if 'addtext' not in raw_sharing_station['hal2option'] or 'objecttyp' not in raw_sharing_station['hal2option']:
      print raw_sharing_station
    else:
      sharing_station.updated = datetime.datetime.now()
      sharing_station.lat = raw_sharing_station['lat']
      sharing_station.lon = raw_sharing_station['lng']
      sharing_station.name = raw_sharing_station['hal2option']['addtext'].replace('Station: ', '')
      sharing_station.station_type = 4
      sharing_station.sharing_provider_id = sharing_provider.id
      db.session.add(sharing_station)
      db.session.commit()