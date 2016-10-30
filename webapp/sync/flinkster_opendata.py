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
import datetime

def sync():
  return
  print "Import Flinkster (OpenData)"
  sharing_provider = SharingProvider.query.filter_by(slug='flinkster_opendata')
  if sharing_provider.count():
    sharing_provider = sharing_provider.first()
  else:
    sharing_provider = SharingProvider()
    sharing_provider.created = datetime.datetime.now()
    sharing_provider.slug = 'flinkster_opendata'
    sharing_provider.active = 1
  
  sharing_provider.updated = datetime.datetime.now()
  sharing_provider.name = 'Flinkster (OpenData)'
  db.session.add(sharing_provider)
  db.session.commit()
  
  with open('stations.csv', 'rt') as csvfile:
    stations = csv.reader(csvfile, delimiter=';', quotechar='\\')
    for row in stations:
      sharing_station = SharingStation.query.filter_by(external_id=row[0]).filter_by(sharing_provider_id=sharing_provider.id)
      if sharing_station.count():
        sharing_station = sharing_station.first()
      else:
        sharing_station = SharingStation()
        sharing_station.created = datetime.datetime.now()
        sharing_station.external_id = row[0]
      sharing_station.updated = datetime.datetime.now()
      
      sharing_station.name = row[2]
      sharing_station.lat = row[19].replace(',', '.').replace('"', '')
      sharing_station.lon = row[18].replace(',', '.').replace('"', '')
      
      sharing_station.station_type = 4
      sharing_station.vehicle_all = 1
      sharing_station.sharing_provider_id = sharing_provider.id
      if sharing_station.lat and sharing_station.lon:
        db.session.add(sharing_station)
        db.session.commit()

  """
  with open('vehicle.csv', 'rt') as csvfile:
    vehicle = csv.reader(csvfile, delimiter=';', quotechar='\\')
    for row in vehicle:
      
        sharing_vehicle = Vehicle
        sharing_vehicle.external_id = row[0]
        sharing_vehicle.manufacturer = row[5]
        sharing_vehicle.model = row[6]
        sharing_vehicle.edition = row[7]
        sharing_vehicle.power = row[10]
        fuel = row[12]
        if "Super" in fuel:
            sharing_vehicle.fuel = "Super"
        elif "Diesel" in fuel:
            sharing_vehicle.fuel = "Diesel"
        elif "Erdgas" in fuel:
            sharing_vehicle.fuel = "Erdgas"
        elif "Strom" in fuel:
            sharing_vehicle.fuel = "Elektro"
        else:
            sharing_vehicle.fuel = "unverified"
        #print(sharing_vehicle.fuel)"""