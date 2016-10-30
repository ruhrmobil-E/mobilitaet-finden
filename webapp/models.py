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

from sqlalchemy.ext.declarative import declarative_base
from webapp import db

Base = declarative_base()

class SharingProvider(db.Model):
  __tablename__ = 'sharing_provider'
  id = db.Column(db.Integer(), primary_key=True)
  
  created = db.Column(db.DateTime())
  updated = db.Column(db.DateTime())
  active = db.Column(db.Integer())
  
  name = db.Column(db.String(255))
  slug = db.Column(db.String(255))
  descr_short = db.Column(db.Text())
  descr = db.Column(db.Text())
  
  email = db.Column(db.String(255))
  website = db.Column(db.String(255))
  licence = db.Column(db.Text())
  
  street = db.Column(db.String(255))
  postalcode = db.Column(db.String(5))
  city = db.Column(db.String(255))
  
  sharing_station = db.relationship("SharingStation", backref="SharingProvider", lazy='dynamic')
  

class SharingStation(db.Model):
  __tablename__ = 'sharing_station'
  id = db.Column(db.Integer(), primary_key=True)
  
  created = db.Column(db.DateTime())
  updated = db.Column(db.DateTime())
  active = db.Column(db.Integer())
  
  name = db.Column(db.String(255))
  slug = db.Column(db.String(255))
  external_id = db.Column(db.String(255))
  
  vehicle_free = db.Column(db.Integer())
  vehicle_all = db.Column(db.Integer())
  station_type = db.Column(db.Integer()) # 1 Fahrrad 2 Lastenrad 3 Fahrradanhänger 4 PKW 5 Transporter 6 Fahrradbox
  
  lat = db.Column(db.Numeric(precision=10,scale=7))
  lon = db.Column(db.Numeric(precision=10,scale=7))
  
  vehicle = db.relationship("Vehicle", backref="SharingStation", lazy='dynamic')
  
  sharing_provider_id = db.Column(db.Integer, db.ForeignKey('sharing_provider.id'))
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Region %r>' % self.name

  
class Vehicle(db.Model):
  __tablename__ = 'vehicle'
  id = db.Column(db.Integer(), primary_key=True)
  created = db.Column(db.DateTime())
  updated = db.Column(db.DateTime())
  active = db.Column(db.Integer())
  
  sharing_station_id = db.Column(db.Integer, db.ForeignKey('sharing_station.id'))
  
  name = db.Column(db.String(255))
  external_id = db.Column(db.String(255))
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Procedure %r>' % self.name


class Region(db.Model):
  __tablename__ = 'region'
  
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(255))
  slug = db.Column(db.String(255), unique=True)
  created = db.Column(db.DateTime())
  updated = db.Column(db.DateTime())
  active = db.Column(db.Integer())
  
  osm_id = db.Column(db.Integer())
  geo_json = db.Column(db.Text())
  rgs = db.Column(db.String(255))
  region_level = db.Column(db.Integer())
  postalcode = db.Column(db.String(255))
  fulltext = db.Column(db.String(255))
  
  lat = db.Column(db.Numeric(precision=10,scale=7))
  lon = db.Column(db.Numeric(precision=10,scale=7))
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Hoster %r>' % self.name
