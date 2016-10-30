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
import json

def sync():
  print "Import Greenwheels"
  base_url = 'https://www.greenwheels.com/book/js/de/citiesAndLocations/'
  r = requests.get(base_url, verify=False)
  cities = json.loads(r.text.encode('utf-8'))
  sharing_provider = SharingProvider.query.filter_by(slug='greenwheels')
  if sharing_provider.count():
    sharing_provider = sharing_provider.first()
  else:
    sharing_provider = SharingProvider()
    sharing_provider.created = datetime.datetime.now()
    sharing_provider.slug = 'greenwheels'
    sharing_provider.active = 1
  
  sharing_provider.updated = datetime.datetime.now()
  sharing_provider.name = 'GreenWheels'
  db.session.add(sharing_provider)
  db.session.commit()
  
  for city in cities:
    for raw_sharing_station in city['locations']:
      sharing_station = SharingStation.query.filter_by(external_id=raw_sharing_station['id']).filter_by(sharing_provider_id=sharing_provider.id)
      if sharing_station.count():
        sharing_station = sharing_station.first()
      else:
        sharing_station = SharingStation()
        sharing_station.created = datetime.datetime.now()
        sharing_station.external_id = raw_sharing_station['id']
      sharing_station.active = 1
      sharing_station.updated = datetime.datetime.now()
      sharing_station.lat = raw_sharing_station['geo'][0]
      sharing_station.lon = raw_sharing_station['geo'][1]
      sharing_station.name = raw_sharing_station['addr']
      sharing_station.vehicle_all = len(raw_sharing_station['cars'])
      sharing_station.station_type = 4
      sharing_station.sharing_provider_id = sharing_provider.id
      db.session.add(sharing_station)
      db.session.commit()